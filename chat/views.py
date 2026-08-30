from django.contrib.auth.models import User
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from django.shortcuts import render

@api_view(["GET"])
def users_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def conversations_list(request):
    conversations = Conversation.objects.all()
    serializer = ConversationSerializer(conversations, many=True)

    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def conversation_messages(request, conversation_id):

    conversation = Conversation.objects.get(id=conversation_id)

    if request.method == "GET":
        messages = conversation.messages.all().order_by("created_at")
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data)

    if request.method == "POST":
        content = request.data.get("content")

        if not content:
            return Response(
                {"error": "Message content is required"},
                status=400
            )

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )

        serializer = MessageSerializer(message)

        return Response(serializer.data, status=201)

@api_view(["POST"])
def login_view(request):

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(
        username=username,
        password=password
    )

    if user is None:
        return Response(
            {"error": "Invalid username or password"},
            status=401
        )

    token, created = Token.objects.get_or_create(user=user)

    return Response({
        "token": token.key,
        "user": UserSerializer(user).data
    })
def chat_page(request):
    return render(request, "chat/chat.html")



def login_page(request):
    return render(request, "chat/login.html")

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_or_create_conversation(request, user_id):
    other_user = User.objects.get(id=user_id)

    if other_user == request.user:
        return Response(
            {"error": "You cannot start a conversation with yourself."},
            status=400
        )

    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)

    serializer = ConversationSerializer(conversation)

    return Response(serializer.data)