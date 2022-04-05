from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('view_score', view_score, name="view_score"),
    path('<int:id>', take_quiz, name="take_quiz"),
]
