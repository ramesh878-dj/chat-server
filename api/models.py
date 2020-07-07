
from django.contrib.auth import get_user_model
from django.db import models

User= get_user_model()

class Testtable(models.Model):
    title = models.TextField(null=True, blank=True)
    username = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Friends_table(models.Model):
    requester_id = models.IntegerField(default=0)
    requester_name= models.CharField(max_length=100, null=False, blank=False)
    accepter_id = models.IntegerField(default=0)
    accepter_name= models.CharField(max_length=100, null=False, blank=False)
    friends_status= models.IntegerField(default=0)
    req_date = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    auto_id= models.IntegerField(default=0)
    sender_name = models.CharField(max_length=100, null=False, blank=False)
    reciever_name = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def last_10_messages():
        return Message.objects.order_by('-timestamp').all()[:10]

class LikeTable(models.Model):
    likeCount=models.IntegerField(default=0)