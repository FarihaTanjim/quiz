from django.shortcuts import render
from .models import *
from django.http import JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def home(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'home.html', context)

@login_required(login_url='/login')
def view_score(request):
    user = request.user
    score = ScoreBoard.objects.filter(user=user)
    context = {'score': score}
    return render(request, 'score.html', context)


@login_required(login_url='/login')
def take_quiz(request, id):
    raw_questions = Question.objects.filter(course =id)[:20]
    context = {'id': id, 'questions' : raw_questions}
    return render(request, 'quiz.html', context)


@csrf_exempt
@login_required(login_url='/login')
def check_score(request):
    data = json.loads(request.body)
    user = request.user
    course_id = data.get('course_id')
    solutions = json.loads(data.get('data'))
    course = Course.objects.get(id=course_id)
    score = 0
    for solution in solutions:
        question = Question.objects.filter(id=solution.get('question_id')).first()

        if (question.answer) == solution.get('option'):
            score = score + question.marks

    score_board = ScoreBoard(course=course, score=score, user=user)
    score_board.save()

    return JsonResponse({'message': 'success', 'status': True})


