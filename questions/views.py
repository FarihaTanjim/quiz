from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required(login_url='/accounts/login')
def home(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'home.html', context)

@login_required(login_url='/accounts/login')
def view_score(request):
    user = request.user
    score = ScoreBoard.objects.filter(user=user)
    context = {'scores': score}
    return render(request, 'score.html', context)


@login_required(login_url='/accounts/login')
def take_quiz(request, id):
    if request.method == "GET" :
        raw_questions = Question.objects.filter(course =id)[:20]
        context = {'id': id, 'questions' : raw_questions}
        return render(request, 'quiz.html', context)
    
    if request.method == "POST":
        data = request.POST
        print(data)
        user = request.user
        course = Course.objects.get(id=id)
        score = 0
        for question in Question.objects.filter(course=course):

            if str(question.answer) == data.get(str(question.id))[0]:
                score = score + question.marks

        score_board = ScoreBoard(course=course, score=score, user=user)
        score_board.save()

        return redirect("/view_score")

