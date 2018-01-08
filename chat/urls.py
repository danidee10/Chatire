"""URL's for the chat app."""

from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('chat/new/', views.NewChatSession.as_view()),
    path('chat/join/', views.JoinChatView.as_view()),
    path('chat/message/<uri>/', views.ChatSessionMessageView.as_view()),
]
