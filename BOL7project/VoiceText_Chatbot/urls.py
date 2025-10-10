
from django.contrib import admin
from django.urls import path
from .import views


urlpatterns=[

    path("",views.chat_page,name="chat_page"),            
    path('api/chat/', views.chat_api, name='chat_api'),               # POST request receive karke LLM call karta hai ✅
    path('generate1/', views.generate_voice, name='generate_voice'),  # POST request receive karke  user ki voice ko Backend ko dena
    path('speech-to-text/', views.speech_to_text_view, name='speech_to_text_view'),  # Get ka use karke Response dena. ✅

    


]