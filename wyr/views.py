from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import User, Question, Vote
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from libgravatar import Gravatar
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from django.utils.html import strip_tags
from django.urls import reverse
import json
import random
import time
from datetime import datetime


def random_question():
    return random.choice(Question.objects.filter(approved=True))


# Create your views here.


def index(request):
    if request.user.is_authenticated != True:
        return HttpResponseRedirect(reverse("login"))
    return render(
        request, "index.html", {
            "question": random_question(),
            "gravatar": Gravatar(request.user.email).get_image(),
            "user": request.user,
            "myquestions": Question.objects.filter(owner=request.user.username)
        })


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        print("e")
        # Attempt to sign user in

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'login.html',
                          {'message': 'Invalid username and/or password.'})
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation

        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'register.html',
                          {'message': 'Passwords must match.'})

        # Attempt to create new user

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'register.html',
                          {'message': 'Username already taken.'})
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'register.html')


trusted = ["ch1ck3n", "UltraBraine X"]


def create(request):
    if request.user.is_authenticated != True:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":
        new = Question()
        new.left = strip_tags(request.POST.get("left"))
        new.right = strip_tags(request.POST.get("right"))
        new.owner = request.user.username
        new.q_id = Question.objects.last().q_id + 1
        new.pub_date = datetime.today().strftime('%Y-%m-%d')
        if request.user.username in trusted:
            new.approved = True
        new.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "create.html")


def profile(request, username):
    if request.user.is_authenticated != True:
        return HttpResponseRedirect(reverse("login"))
    return render(
        request, "profile.html", {
            "user":
            list(filter(lambda x: x.username == username,
                        User.objects.all()))[0],
            "myquestions":
            list(reversed(Question.objects.filter(owner=username))),
            "gravatar":
            Gravatar(
                list(
                    filter(lambda x: x.username == username,
                           User.objects.all()))[0].email).get_image(),
        })


def percent(num1, num2):
    num1 = float(num1)
    num2 = float(num2)
    percentage = (num1 / num2 * 100)
    return percentage


def api(request, category, action):
    if request.user.is_authenticated != True:
        return HttpResponseRedirect(reverse("login"))
    if category == "question":
        if action == "random":
            time.sleep(0.5)
            if request.GET.get("all") == "true":
                return JsonResponse(
                    model_to_dict(random.choice(Question.objects.all()),
                                  json_dumps_params={'indent': 2}))
            return JsonResponse(model_to_dict(random_question()),
                                json_dumps_params={'indent': 2})
        if action == "recent":
            if request.GET.get("all") == "true":
                return JsonResponse(model_to_dict(
                    Question.objects.all().last()),
                                    json_dumps_params={'indent': 2})
            return JsonResponse(model_to_dict(
                Question.objects.filter(approved=True).last()),
                                json_dumps_params={'indent': 2})
        if action == "vote":
            time.sleep(0.5)
            if Vote.objects.filter(q_id=int(request.GET.get("id")),
                                   voter=request.user.username).count() != 0:
                return JsonResponse({
                    "error":
                    "av",
                    "status":
                    "false",
                    "data":
                    model_to_dict(
                        Question.objects.filter(
                            q_id=int(request.GET.get("id")))[0])
                })
            question = Question.objects.filter(
                q_id=int(request.GET.get("id")))[0]
            vote = Vote()
            vote.q_id = int(request.GET.get("id"))
            vote.side = request.GET.get("side")
            vote.voter = request.user.username
            vote.save()
            question.votes += 1
            if request.GET.get("side") == "left":
                question.vt_l2 += 1
                question.vt_l = round(percent(question.vt_l2, question.votes))
                question.vt_r = round(percent(question.vt_r2, question.votes))
            elif request.GET.get("side") == "right":
                question.vt_r2 += 1
                question.vt_l = round(percent(question.vt_l2, question.votes))
                question.vt_r = round(percent(question.vt_r2, question.votes))
            question.save()
            username = request.user.username
            user = list(
                filter(lambda x: x.username == username,
                       User.objects.all()))[0]
            user.votes += 1
            user.save()
            return JsonResponse({
                "status": "true",
                "data": model_to_dict(question)
            })
        if action == "approve":
            if request.user.username == "ch1ck3n":
                question = Question.objects.filter(
                    q_id=request.GET.get("id"))[0]
                question.approved = True
                question.save()
                return JsonResponse({"sucess": "true"})
            return JsonResponse({"sucess": "false"})
        if action == "bababooey":
            for z in Vote.objects.filter(q_id=80):
                print(model_to_dict(z))
            return HttpResponse(json.dumps(Vote.objects.filter(q_id=80)))
    return HttpResponse("Welcome to the api endpoint, hacker.")


def all(request):
    if request.user.is_authenticated != True:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "all.html",
                  {"questions": Question.objects.all().order_by('-q_id')[:20]})


def questions(request, q):
    if request.user.is_authenticated != True:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "all.html",
                  {"questions": Question.objects.all().order_by('-q_id')[:q]})


def moderate(request, function):
    if request.user.username in ["ch1ck3n"]:
        if function == "approve":
            return render(
                request, "all.html", {
                    "questions":
                    Question.objects.filter(approved=False).order_by('-q_id')
                })
