=> BOL7 AI Chatbot (Gemini + Vosk + gTTs + RAG + POSTGRESQL)

This is a Django-based AI Voice Chatbot project. It can listen, think, and speak — using Gemini (LLM), Vosk (STT), and gTTS (TTS)., RAG

Project Name — (e.g. BOL7 AI Chatbot) ✅ Features — (LLM, TTS, STT, RAG with PostgreSQL, Django Backend, etc.) Tech Stack — (Python, Django, Gemini API, Vosk, gTTS, PostgreSQL) correct?

Project Pecularity 🔴 we are Using of Gemini 2.5 Flash model. 🔴 it understand multiple language. 🔴 it can talk to you voice-to-voice Also Messages-to-messages. 🔴 We Did Use OF RAG => Retrieval Argumented Generation .

utils.py

Ye file logic aur helper functions ke liye hoti hai. Matlab: jo kaam backend me core logic ke liye hota hai

LLM call (Gemini) Text-to-speech (gTTS) Speech-to-text (VOSK)

💫 Views sirf data bhejta aur laata hai, Utils actual kaam karta hai.

views.py

Ye Kabel files ko request/response handle karne ke liye hota hai. Matlab: frontend se jo data aata hai (POST/GET), usko receive karna, utils ke functions call karna, aur response return karna.

Views me direct business logic nahi likhna chahiye (best practice), sirf utils ko call karke result return karna.
<img width="908" height="826" alt="image" src="https://github.com/user-attachments/assets/bc7235dc-b25c-46aa-9ad8-6ae1acb7159a" />







