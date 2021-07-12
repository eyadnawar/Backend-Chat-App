from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addClient/', views.addClient),
    path('addOperator/', views.addOperator),
    path('startChat/', views.startChat),
    path('getConversation/<conversation_id>/', views.getConversation)
]