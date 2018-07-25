from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from rest_framework.response import Response
from django.contrib import auth
from django.contrib.auth import authenticate
# Create your views here.
import traceback
@api_view(["GET","POST"])
def sign_up(request):

    try:
        username = request.data.get("username")
        password = request.data.get("password")
        age = request.data.get("age")

        all_user_objects = User.objects.all()
        all_username = [i.username for i in all_user_objects]
        if username in all_username:
            return Response({"response_text":"duplicate"})

        else:
            user_object = User(username=username,password=password)
            user_object.set_password(user_object.password)
            user_object.save()

            kotha_user = Kotha_user(username=username,user=user_object,age=age)
            kotha_user.save()
            logged_in_object = Logged_in_users(username=username)
            logged_in_object.save()
            return Response({"response_text":"successful"})
    except:
        return Response({"response_text":"error"})

@api_view(["GET","POST"])
def login(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        print(user)
        if user is None:
            return Response ({"response_text":"mismatched"})
        else:
            login_object = Logged_in_users(username=username)
            login_object.save()
            return Response({"response_text":"successful"})
    except:
        return Response({"response_text":"error"})

@api_view(["GET","POST"])
def send_message(request):
    try:
        username=request.data.get("sender")
        word = request.data.get("message")
        to = request.data.get("receiver")

        try:
            if len(username.strip())==0 or len(word.strip())==0 or len(to.strip())==0:
                return Response({"response_text":"error"})
        except Exception as ex:
            return Response({"response_text":"error"})

        try:
            sender = Kotha_user.objects.get(username=username)
        except Exception as ex:
            print(traceback.print_exc())
            return Response({"response_text":"error"})
        try:
            receiver = Kotha_user.objects.get(username = to)
        except Exception as ex:
            print(traceback.print_exc())
            return Response({"response_text":"no receiver"})
        blocked_list = Blocked_list.objects.filter(blocked_by=receiver,block_to=sender)

        if len(blocked_list)>0:
            return Response({"response_text":"block"})

        word = Words(message_by=sender,message_to=receiver,word=word)
        word.save()
        return Response({"response_text":"successful"})
    except Exception as ex:
        print(ex)
        return Response({"response_text":"error"})

@api_view(["GET","POST"])
def my_all_message(request):
    username = request.data.get("username")
    kotha_user = Kotha_user.objects.get(username=username)
    all_messages = Words.objects.filter(message_to=kotha_user)
    all_texts = [(i.word,i.message_by_id) for i in all_messages]
    return Response({"all_texts":all_texts[::-1]})

@api_view(["GET","POST"])
def block(request):
    try:
        username = request.data.get("username")
        blocked_id = request.data.get("blocked_id")
        print(blocked_id)
        kotha_object = Kotha_user.objects.get(username=username)
        blocked_object = Kotha_user.objects.get(id=blocked_id)

        block = Blocked_list(block_to=blocked_object,blocked_by=kotha_object)
        block.save()

        return Response({"response_text":"successful"})
    except:
        print(traceback.print_exc())
        return Response({"response_text":"error"})

@api_view(["GET","POST"])
def reply(request):
    try:
        username=request.data.get("sender")
        word = request.data.get("message")
        to = request.data.get("receiver_id")

        try:
            if len(username.strip())==0 or len(word.strip())==0:
                return Response({"response_text":"error"})
        except Exception as ex:
            return Response({"response_text":"error"})

        try:
            sender = Kotha_user.objects.get(username=username)
        except Exception as ex:
            print(traceback.print_exc())
            return Response({"response_text":"error"})
        try:
            receiver = Kotha_user.objects.get(id=to)
        except Exception as ex:
            print(traceback.print_exc())
            return Response({"response_text":"no receiver"})
        blocked_list = Blocked_list.objects.filter(blocked_by=receiver,block_to=sender)

        if len(blocked_list)>0:
            return Response({"response_text":"block"})

        word = Words(message_by=sender,message_to=receiver,word=word)
        word.save()
        return Response({"response_text":"successful"})
    except Exception as ex:
        print(ex)
        return Response({"response_text":"error"})

