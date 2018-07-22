from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from rest_framework.response import Response
from django.contrib import auth
from django.contrib.auth import authenticate
# Create your views here.
@api_view(["GET","POST"])
def sign_up(request):
    username = request.data.get("username")
    password = request.data.get("password")

    all_user_objects = User.objects.all()
    all_username = [i.username for i in all_user_objects]
    if username in all_username:
        return Response({"response_text":"duplicate"})

    else:
        user_object = User(username=username,password=password)
        user_object.set_password(user_object.password)
        user_object.save()

        kotha_user = Kotha_user(username=username,user=user_object)
        kotha_user.save()
        return Response({"response_text":"successful"})

@api_view(["GET","POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is None:
        return Response ({"mismatched"})
    else:
        auth.login(request,user)
        return Response({"response_text":"successful"})

@api_view(["GET","POST"])
def send_message(request):
    username=request.data.get("username")
    word = request.data.get("word")
    to = request.data.get("to")
    sender = Kotha_user.objects.get(username=username)
    receiver = Kotha_user.objects.get(receiver = to)
    blocked_list = Blocked_list.objects.filter(blocked_by=receiver,block_to=sender)
    if len(blocked_list)>0:
        return Response({"response_text":"block"})
    word = Words(message_by=sender,message_to=receiver,word=word)
    word.save()
    return Response({"response_text":"successful"})

@api_view(["GET","POST"])
def my_all_message(request):
    username = request.data.get("username")
    kotha_user = Kotha_user.objects.get(username=username)
    all_messages = Words.objects.filter(message_to=kotha_user)
    all_texts = [i.word for i in all_messages]
    return Response({"all_texts":all_texts})

@api_view(["GET","POST"])
def block(request):
    username = request.data.get("username")
    word = request.data.get("word")
    kotha_object = Kotha_user.objects.get(username=username)

    all_senders = Words.objects.filter(message_to=kotha_object,word=word)

    for i in all_senders:
        block =Blocked_list(block_to=i,blocked_by=kotha_object)
        block.save()
    return Response({"response_text":"successful"})

