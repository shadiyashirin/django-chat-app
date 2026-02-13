from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db.models import Count

from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer

User = get_user_model()


class CreateOrGetChatRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        other_user_id = request.data.get("user_id")

        if not other_user_id:
            return Response(
                {"error": "user_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        current_user = request.user

        if current_user == other_user:
            return Response(
                {"error": "Cannot create room with yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if room already exists
        rooms = ChatRoom.objects.filter(
            participants=current_user
            ).filter(participants=other_user).distint()

        for room in rooms:
            if room.participants.count() == 2:
                serializer = ChatRoomSerializer(room)
                return Response(serializer.data)


        # Create new room
        room = ChatRoom.objects.create()
        room.participants.add(current_user, other_user)

        serializer = ChatRoomSerializer(room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        room_id = request.data.get("room")
        text = request.data.get("text")

        if not room_id or not text:
            return Response(
                {"error": "room_id and text are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            room = ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return Response(
                {"error": "Chat room not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if user is participant
        if request.user not in room.participants.all():
            return Response(
                {"error": "You are not a participant of this room"},
                status=status.HTTP_403_FORBIDDEN
            )

        message = Message.objects.create(
            room=room,
            sender=request.user,
            text=text
        )

        serializer = MessageSerializer(message)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class ChatHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        try:
            room = ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return Response(
                {"error": "Room not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user not in room.participants.all():
            return Response(
                {"error": "You are not a participant of this room"},
                status=status.HTTP_403_FORBIDDEN
            )

        messages = room.messages.all().order_by("timestamp")
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data)
