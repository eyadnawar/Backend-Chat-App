from django.db import models

# Create your models here.

class Client(models.Model):
    client_id = models.IntegerField(primary_key= True, db_index= True)
    username = models.CharField(max_length=20)
    location = models.CharField(max_length=20)

class Operator(models.Model):
    operator_id = models.IntegerField(primary_key= True, db_index= True)
    operator_name = models.CharField(max_length=20)
    operator_group = models.CharField(max_length=20)
    store_id = models.IntegerField()

class Conversation(models.Model):
    conversation_id = models.IntegerField(primary_key= True, db_index= True)
    store_id = models.IntegerField()
    operator_id = models.IntegerField()
    client_id = models.IntegerField()
    operator_group = models.CharField(max_length=20)

class Chat(models.Model):
    chat_id = models.IntegerField(primary_key= True, unique= True, db_index= True)
    conversation_id = models.IntegerField()
    payload = models.CharField(max_length=300)
    client_id = models.IntegerField()
    operator_id = models.IntegerField()
    utc_date = models.DateTimeField()
    status = models.CharField(max_length=4)

