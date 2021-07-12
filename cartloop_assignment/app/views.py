from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers
from .serializers import *
from datetime import datetime
import re
import json
from django.forms.models import model_to_dict

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the conversation index.")

@api_view(['POST'])
def addClient(request):
    serializer = ClientSerializer(data= request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def addOperator(request):
    serializer = OperatorSerializer(data= request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def startChat(request):
    serializer = ChatSerializer(data= request.data)
    if serializer.is_valid():
        try:
            client = Client.objects.get(client_id= request.data['client_id'])
            operator = Operator.objects.get(operator_id= request.data['operator_id'])
            payload = request.data['payload']
            if(re.search("{{ username }}", payload)):
                new_payload = payload.replace("{{ username }}", Client.objects.get(client_id= request.data['client_id']).username)
            elif(re.search("{{ operator }}", payload)):
                new_payload = payload.replace("{{ operator }}", Operator.objects.get(operator_id= request.data['operator_id']).operator_name)
            else:
                pass
            chat_object = Chat(
                conversation_id= request.data['conversation_id'],
                client_id= request.data['client_id'],
                operator_id= request.data['operator_id'],
                payload= new_payload,
                chat_id= request.data['chat_id'],
                utc_date= datetime.utcnow(),
                status= 'new'
            )
        except:
            return Response({
                'message': 'The user or the client id may be wrong',
                'status': 400
            })
        try:
            conversation = Conversation.objects.get(conversation_id= request.data['conversation_id'])
            chat_object.save()
            return Response({
                'message': 'success, your message has been sent',
                'status': 200
            })
        except:
            conv_serializer = ConversationSerializer(data= request.data)
            conv_object = Conversation(
                conversation_id= request.data['conversation_id'],
                client_id= request.data['client_id'],
                operator_id= request.data['operator_id'],
                operator_group= Operator.objects.get(operator_id= request.data['operator_id']).operator_group,
                store_id= Operator.objects.get(operator_id= request.data['operator_id']).store_id
            )
            chat_object.save()
            conv_object.save()
            return Response({
                'message': 'success, your message has been added to the conversation.',
                'status': 200
            })
    else:
        return Response({
            'message': "Request error. The request is non-serializable.",
            'status': 400
        })

@api_view(["GET"])
def getConversation(request, conversation_id):
    try:
        Conversation.objects.get(conversation_id= int(conversation_id))
        chat_list = [chat for chat in Chat.objects.all() if chat.conversation_id == int(conversation_id)]
        final_chat_list = []
        for chat in chat_list:
            final_chat_list.append(model_to_dict(chat))
        conversation_object = {
            'conversation_id': int(conversation_id),
            'store_id': Operator.objects.get(operator_id=chat_list[0].operator_id).store_id,
            'operator_id': chat_list[0].operator_id,
            'client_id': chat_list[0].client_id,
            'operator_group': Operator.objects.get(operator_id=chat_list[0].operator_id).operator_group,
            'chat': final_chat_list
        }
        return Response({
            'conversation': conversation_object,
            'status': 200
        })
    except:
        return Response({
            'message': 'There is no conversation with the specified id.',
            'status': 404
        })

