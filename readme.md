# Description

This project is a chat-like app that facilitates communication between clients and store operators.
Our postgres database acts as a message queue for this one.

This system which acts as a Network Service for communication through a REST API performs 4 operations:
* Add a client 
  
* Add an operator.
  
* Start a chat between a client and a store operator
  
* Retrieve a conversation between a client and a store operator

## Building, Testing, Running, and Connecting to the Service

This system is implemented in Python's Django. It uses Python version 3.9.4 and Django version 3.2.5. To build, just clone the repo by running the following command in Git Bash in the appropriate directory:

git clone https://github.com/eyadnawar/Cartloop_Assignment.git

Open the terminal and activate the virtual environment via the command `.\venv\Scripts\activate.bat` then install the necessary packages in the [requirements.txt](https://github.com/eyadnawar/kausa-task/blob/master/requirements.txt) run `pip install -r requirements.txt`, then `cd cartloop_assignment` into cartloop_assignment directory and finally run `manage.py runserver`. It will run on the localhost.

To conect to the service, there are 4 endpoints that correspond to each of the aforementioned operations. These endpoints are:

* `/app/addClient/` which is a `POST` method. The endpoint receives the following parameters in the body of the request:

    1. `client_id`: IntegerField (primary key, database index, unique)### The client ID
    2. `username`: CharField                                          ### The client name
    3. `location`: CharField                                          ### The client's location
       
        and returns a response with the client created
    
* `/app/addOperator/` which is a `POST` method. The endpoint receives the following parameters in the body of the request:

    1. `operator_id`: IntegerField (primary key, database index, unique)### The operator ID
    2. `operator_name`: CharField                                       ### The operator name
    3. `operator_group`: CharField                                      ### The operator group
    4. `store_id`: IntegerField                                         ### The operator's store ID
       
        and returns a response with the operator created

* `/app/startChat/` which is a `POST` method. The endpoint receives the following parameters in the body of the request:

    1. `chat_id`: IntegerField (primary key, database index, unique) ### The chat ID, could also be changed to UUID to facilitate chat id generation automation
    2. `conversation_id`: IntegerField                               ### The conversation ID
    3. `payload`: CharField (less than 300 characters)               ### The message to be sent
    4. `client_id`: IntegerField                                     ### The client's ID
    5. `opertor_id`: IntegerField                                    ### The operator's ID
       
        and returns a response with the chat created
       
* `/app/getConversation/<id>/` which is a `GET` method. The endpoint receives the ID of the desired conversation in the request url:
       
        and returns a response with the desired conversation with all the chats involved

## Technical *(Implementation)* Details

This system is built in Python's `Django`, and uses `PostgreSQL` as its database storage system.

## Potential Features

A potential Feature could be to use a scheduler to auto-send messages which have been sent out of working hours (9:00 am - 2:00 pm).

It is also worth noting that an XMPP protocol would be better suited for communication more than an its HTTP counterpart.
The reason being that in an HTTP protocol, the server cannot send un-asked-for messages, it can only respond to requests, which means than a user (client or operator) to check whether they have any messages, they must keep polling the server, which in-turn polls the database. This is a huge load on the db. A better approach would be to use a streaming technique instead, in which a communication between the client and the server is established only once and the channel is then kept open and the server pushes messages through this channel.
An example of this implementation may be the publisher-subscriber model, which are more formally known as Message Queues. An example would be RabbitMQ or AMQP.
