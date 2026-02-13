from django.urls import path
from .views import CreateOrGetChatRoomView, SendMessageView, ChatHistoryView

urlpatterns = [
    path('room/', CreateOrGetChatRoomView.as_view(), name='create_or_get_room'),
    path('send/', SendMessageView.as_view(), name='send_message'),
    path('history/<int:room_id>/', ChatHistoryView.as_view(), name='chat_history'),
]