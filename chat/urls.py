from django.urls import path
from . import views


urlpatterns = [
    path("users/", views.users_list),
    path("conversations/", views.conversations_list),
    path(
        "conversations/<int:conversation_id>/messages/",
        views.conversation_messages
    ),
    path("login/", views.login_view),
    path(
    "conversations/with/<int:user_id>/",
    views.get_or_create_conversation),
    path("login-page/", views.login_page),
    
]