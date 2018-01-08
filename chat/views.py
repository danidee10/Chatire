"""Views for the chat app."""

from django.contrib.auth import get_user_model
from .models import ChatSession, ChatSessionMember, ChatSessionMessage

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions


class NewChatSession(APIView):
    """Manage Chat sessions."""

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """create a new chat session."""
        user = request.user

        chat_session = ChatSession.objects.create(owner=user)

        return Response({
            'status': 'SUCCESS', 'uri': chat_session.uri,
            'message': 'New chat session created'
        })


class JoinChatView(APIView):
    """Allow a user to join a Chat Session."""

    permission_classes = (permissions.IsAuthenticated,)

    def deserialize_user(self, user):
        """Deserialize user instance to JSON."""
        return {
            'id': user.id, 'username': user.username, 'email': user.email,
            'first_name': user.first_name, 'last_name': user.last_name
        }
        
    def put(self, request, *args, **kwargs):
        """Handle the POST request."""
        uri = request.data['uri']
        user = request.user

        chat_session = ChatSession.objects.get(uri=uri)

        chat_session.members.get_or_create(
            user=user, chat_session=chat_session
        )

        owner = self.deserialize_user(chat_session.owner)
        members = [
            self.deserialize_user(chat_session.user) 
            for chat_session in chat_session.members.all()
        ]
        members.insert(0, owner)  # Make the owner the first member

        return Response ({
            'status': 'SUCCESS', 'members': members,
            'message': '%s joined that chat' % user.username
        })


class ChatSessionMessageView(APIView):
    """Create/Get Chat session messages."""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """return all messages in a chat session."""
        uri = kwargs['uri']

        chat_session = ChatSession.objects.get(uri=uri)
        messages = [chat_session_message.to_json() 
            for chat_session_message in chat_session.messages.all()]

        return Response({
            'id': chat_session.id, 'uri': chat_session.uri,
            'messages': messages
        })

    def post(self, request, *args, **kwargs):
        """create a new message in a chat session."""
        uri = kwargs['uri']
        message = request.data['message']

        user = request.user
        chat_session = ChatSession.objects.get(uri=uri)

        ChatSessionMessage.objects.create(
            user=user, chat_session=chat_session, message=message
        )

        return Response ({
            'status': 'SUCCESS', 'uri': chat_session.uri, 'message': message
        })
