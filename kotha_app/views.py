from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from rest_framework.response import Response
from django.contrib import auth
from django.contrib.auth import authenticate
# Create your views here.
from django.utils import timezone
import traceback

def check_login(username):
    logged_in_objects = Logged_in_users.objects.all()
    logged_in_usernames = [i.username.lower() for i in logged_in_objects]
    if username.lower() in logged_in_usernames:
        return True
    else:
        return False

@api_view(["GET","POST"])
def sign_up(request):

    try:
        username = request.data.get("username")
        password = request.data.get("password")
        age = request.data.get("age")

        all_user_objects = User.objects.all()
        all_username = [i.username.lower() for i in all_user_objects]
        if username.lower() in all_username:
            return Response({"response_text":"duplicate"})

        else:
            print(password)
            user = User(username=username,date_joined=timezone.now(),first_name=password)
            user.set_password(password)
            user.save()

            kotha_user = Kotha_user(username=username,user=user,age=age)
            kotha_user.save()
            temp_logged_objects = Logged_in_users.objects.filter(username = username)
            temp_logged_objects.delete()

            logged_in_object = Logged_in_users(username=username)
            logged_in_object.save()
            return Response({"response_text":"successful"})
    except:
        print(traceback.print_exc())
        return Response({"response_text":"error"})

@api_view(["GET","POST"])
def login(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")

        print(username)
        print(password)

        user = auth.authenticate(username=username,password=password)
        print(user)
        # user_from_databse =User.objects.get(username=username)
        # user=password==user_from_databse.first_name

        if user is None:
            return Response ({"response_text":"mismatched"})
        else:
            temp_logged_objects = Logged_in_users.objects.filter(username=username)
            temp_logged_objects.delete()

            login_object = Logged_in_users(username=username)
            login_object.save()
            return Response({"response_text":"successful"})
    except:
        return Response({"response_text":"error"})

@api_view(["GET","POST"])
def send_message(request):

    username = request.data.get("sender")
    try:
        if check_login(username):
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
    except:
        return Response({"response_text": "failed"})

@api_view(["GET","POST"])
def my_all_message(request):

    username = request.data.get("username")
    try:
        if check_login(username):
            username = request.data.get("username")
            kotha_user = Kotha_user.objects.get(username=username)
            all_messages = Words.objects.filter(message_to=kotha_user)
            all_texts = [(i.word,i.message_by_id) for i in all_messages]
            return Response({"all_texts":all_texts[::-1]})
        return Response({"all_texts": []})
    except:
        return Response({"response_text": "failed"})

@api_view(["GET","POST"])
def check_block(request):

    username = request.data.get("username")
    try:
        print(username)
        print(check_login(username))
        if check_login(username):

            username =request.data.get("username")
            blocked_id = request.data.get("blocked_id")

            try:
                sender_object = Kotha_user.objects.get(username=username)
                blocked_object = Blocked_list.objects.filter(block_to_id=blocked_id,blocked_by_id=sender_object.id)
                if len(blocked_object)>0:
                    return Response({"response_text":"1"})
                else:
                    return Response({"response_text": "0"})
            except:
                return Response({"response_text": "0"})
    except:
        return Response({"response_text": "failed"})

@api_view(["GET","POST"])
def sent_messages(request):

    username =  request.data.get("username")
    print(username)
    try:
        if check_login(username):
            username = request.data.get("username")
            kotha_user = Kotha_user.objects.get(username=username)
            all_messages = Words.objects.filter(message_by=kotha_user)
            all_text = []
            for i in all_messages:
                receiver = Kotha_user.objects.get(id =i.message_to_id)
                all_text.append((i.word,receiver.username))
            return Response({"all_texts":all_text[::-1]})
    except:
        return Response({"response_text": "failed"})

@api_view(["GET","POST"])
def block(request):
    username =request.data.get("username")
    print(username)
    try:
        if check_login(username):
            task =request.data.get("task")
            username = request.data.get("username")
            blocked_id = request.data.get("blocked_id")
            if task=="Block Sender":
                try:
                    kotha_object = Kotha_user.objects.get(username=username)
                    blocked_object = Kotha_user.objects.get(id=blocked_id)

                    block = Blocked_list(block_to=blocked_object,blocked_by=kotha_object)
                    block.save()

                    return Response({"response_text":"successful"})
                except:
                    print(traceback.print_exc())
                    return Response({"response_text":"error"})
            else:
                try:
                    blocked_object = Kotha_user.objects.get(id=blocked_id)
                    kotha_object = Kotha_user.objects.get(username=username)
                    all_objects = Blocked_list.objects.filter(block_to=blocked_object,blocked_by=kotha_object)
                    all_objects.delete()
                    return Response({"response_text":"successful"})
                except:
                    return Response({"response_text":"error"})
    except:
        return Response({"response_text": "failed"})

@api_view(["GET","POST"])
def reply(request):
    username = request.data.get("sender")
    print(username)
    try:
        if check_login(username):
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
    except:
        return Response({"response_text": "failed"})

@api_view(["GET","POST"])
def logout(request):
    username = request.data.get("username")
    try:
        if check_login(username):
            print("hello")
            temp_logged_objects = Logged_in_users.objects.filter(username=username)
            temp_logged_objects.delete()
            return  Response({"response_text":"successful"})
        return Response({"response_text": "successful"})
    except:
        return Response({"response_text": "failed"})


