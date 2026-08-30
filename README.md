# Real-Time Chat Application

A real-time web chat application built with Django, Django REST Framework, and Django Channels.

The application allows authenticated users to connect with other users, create conversations, and exchange messages instantly using WebSockets.

## 🚀 Features

- User authentication
- Token-based authentication using Django REST Framework
- User listing
- One-to-one conversations
- Real-time messaging with WebSockets
- Django Channels integration
- Persistent message storage
- Message timestamps
- Current-user message alignment
- Online/offline status
- Conversation history
- WebSocket authentication
- Responsive chat interface

## 🛠️ Tech Stack

### Backend

- Python
- Django
- Django REST Framework
- Django Channels
- Daphne
- WebSockets

### Frontend

- HTML
- CSS
- JavaScript

### Database

- SQLite for local development
- Django ORM

### Development Tools

- Git
- GitHub
- VS Code

## 📁 Project Structure

```text
real-time-chat-app/
│
├── chat/
│   ├── migrations/
│   ├── templates/
│   │   └── chat/
│   │       ├── chat.html
│   │       └── login.html
│   ├── admin.py
│   ├── apps.py
│   ├── consumers.py
│   ├── middleware.py
│   ├── models.py
│   ├── routing.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md