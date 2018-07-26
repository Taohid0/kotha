from django.contrib import admin
from kotha_app.models import *
# Register your models here.

admin.site.register(Kotha_user)
admin.site.register(Words)
admin.site.register(Blocked_list)
admin.site.register(Logged_in_users)
