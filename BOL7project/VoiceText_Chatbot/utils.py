from google import genai
from django.conf import settings
import os
from gtts import gTTS
import wave
import json
from vosk import Model, KaldiRecognizer
import time
from .models import CompanyInfo




# Gemini Client Setup
client = genai.Client(api_key=settings.GEMINI_API_KEY) 





#💫Gemini (LLM) function

def get_gemini_response(user_message):
    if not user_message:
        return "Please type something!"

    prompt = "Please reply in short, maximum 2 sentences: " + user_message
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[{"parts":[{"text": prompt}]}]
    )
    
    return response.text or "Sorry, I couldn't respond."







# 💫TTS function (gTTS)


def text_to_speech_url(message):
    if not message:
        return ""
    try:
        filename = f"voice_{int(time.time()*1000)}.mp3"
        audio_path = os.path.join(settings.MEDIA_ROOT, filename)
        tts = gTTS(text=message, lang='en', slow=False)
        tts.save(audio_path)
        print("Audio saved at:", audio_path)  # <-- Add this for debugging
        return settings.MEDIA_URL + filename
    except Exception as e:
        print("TTS Error:", e)
        return ""





# 💫STT function (VOSK)

VOSK_MODEL_PATH = r"C:\Users\komal\Downloads\vosk-model-small-en-us-0.15"
vosk_model = Model(VOSK_MODEL_PATH)

def speech_to_text(audio_file):
    temp_path = "temp_audio.wav"
    with open(temp_path, "wb") as f:
        for chunk in audio_file.chunks():
            f.write(chunk)
    
    wf = wave.open(temp_path, "rb")
    rec = KaldiRecognizer(vosk_model, wf.getframerate())
    
    result_text = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            result_text += res.get("text", "") + " "
    
    final_res = json.loads(rec.FinalResult())
    result_text += final_res.get("text", "")
    
    wf.close()
    os.remove(temp_path)
    
    return result_text.strip()







# 💫 RAG Function
COMPANY_KEYWORDS = [
    "bol7", "company", "technologies", "sector", "career", "owner", 
    "BOL7 Technologies", "Owner", "Client", "Clients", "Vacancy", 
    "Vacancies", "Employee", "Employees", "Services", "Service",
    "Job", "Jobs", "Hiring", "Recruitment", "Staff", "Team", 
    "Location", "Headquarters", "Founder", "CEO", "Contact", "Apply","Employee Salary","salary"
]

def get_rag_response(user_message):
    try:
        user_message_lower = user_message.lower()

        # Fetch all topics and contents from DB
        all_entries = CompanyInfo.objects.all()  # id, topic, content
        
        # Find all relevant entries matching user query keywords
        matched_contents = []
        for entry in all_entries:
            topic_lower = entry.topic.lower()
            if topic_lower in user_message_lower or topic_lower.split()[0] in user_message_lower:
                matched_contents.append(entry.content)
        
        # If any DB entry matches
        if matched_contents:
            # Combine all relevant content
            db_content = "\n".join(matched_contents)
            prompt = f"User asked: {user_message}\nAnswer using this company info naturally: {db_content}"
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[{"parts":[{"text": prompt}]}]
            )
            return response.text or db_content

        # Otherwise, normal LLM
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[{"parts":[{"text": user_message}]}]
        )
        return response.text or "Sorry, I couldn't respond."

    except Exception as e:
        print("RAG Error:", e)
        return "Sorry, something went wrong."