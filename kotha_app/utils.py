from kotha_app.models import *

def check_login(username):
    logged_in_objects = Logged_in_users.objects.all()
    logged_in_usernames = [i.username.lower() for i in logged_in_objects]
    if username.lower in logged_in_usernames:
        return True
    else:
        return False
