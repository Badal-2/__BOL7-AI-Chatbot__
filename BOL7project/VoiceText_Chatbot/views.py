from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .utils import get_gemini_response, text_to_speech_url, speech_to_text , get_rag_response
import json




def chat_page(request):
    return render(request, "Bol7.html")     #  Messages sends  from the frontend to the backend. 



# 💫 LLM API
@csrf_exempt
def chat_api(request):                        # User ka text frontend se leta hai → Gemini LLM ko bhejta hai → reply deta hai
    if request.method == "POST":              # Ye check karta hai ki frontend se request POST type ki hai ya nahi.                 
        try:  
            data = json.loads(request.body)
            user_message = data.get("response", "")
            bot_reply = get_gemini_response(user_message)  
            return JsonResponse({"response": bot_reply})
        except Exception as e:
            print("LLM Error:", e)
            return JsonResponse({"response": "Something went wrong."})
    return JsonResponse({"response": "Only POST requests are allowed."})






# 🟢 TTS 
@csrf_exempt
def generate_voice(request):
    if request.method == "POST": 
        try:
            message = request.POST.get("message", "")
            if not message:
                return JsonResponse({"voice_url": ""})
            
            voice_url = text_to_speech_url(message)
            return JsonResponse({"voice_url": voice_url})
        except Exception as e:
            print("TTS Error:", e)
            return JsonResponse({"voice_url": ""})
    return JsonResponse({"voice_url": ""})




# 🟢 STT 
@csrf_exempt
def speech_to_text_view(request):
    if request.method == "POST":                    #Ye check karta hai ki frontend se request POST type ki hai ya nahi.
        try:
            audio_file = request.FILES.get("audio")
            if not audio_file:
                return JsonResponse({"text": ""})
            
            result_text = speech_to_text(audio_file)  # utils.py STT function
            return JsonResponse({"text": result_text})
        except Exception as e:
            print("STT Error:", e)
            return JsonResponse({"text": ""})
    return JsonResponse({"text": ""})












# RAG 

@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("response", "")
            bot_reply = get_rag_response(user_message)  # RAG function
            return JsonResponse({"response": bot_reply})
        except Exception as e:
            print("Error:", e)
            return JsonResponse({"response": "Something went wrong."})
    return JsonResponse({"response": "Only POST requests are allowed."})