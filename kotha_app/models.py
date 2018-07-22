from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Kotha_user(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    username= models.CharField(max_length=25)
    is_deleted= models.BooleanField(default=False)

class Blocked_list(models.Model):
    id = models.AutoField(primary_key=True)
    blocked_by = models.ForeignKey(Kotha_user,on_delete=models.DO_NOTHING,related_name="blocked_by")
    block_to  = models.ForeignKey(Kotha_user,on_delete=models.DO_NOTHING,related_name="block_to")
    is_deleted = models.BooleanField(default=False)

class Words(models.Model):
    id = models.AutoField(primary_key=True)
    message_by = models.ForeignKey(Kotha_user,on_delete=models.DO_NOTHING,related_name="message_by")
    message_to = models.ForeignKey(Kotha_user,on_delete=models.DO_NOTHING,related_name="message_to")
    word = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)