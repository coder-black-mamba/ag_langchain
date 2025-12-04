# views.py
from .models import ChatSession
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from .agent import agent, Context

@login_required
def create_session(request):
    session = ChatSession.objects.create(user=request.user)
    return JsonResponse({
        "session_id": str(session.session_id),
        "name": session.name
    })




@login_required
def chat_view(request, session_id):
    body = json.loads(request.body.decode())
    message = body.get("message")

    # Load the session from DB
    session = ChatSession.objects.get(user=request.user, session_id=session_id)

    # CREATE MULTI-SESSION THREAD ID
    thread_id = session.thread_id()

    config = {"configurable": {"thread_id": thread_id}}
    context = Context(user_id=str(request.user.id))

    response = agent.invoke(
        {"messages": [{"role": "user", "content": message}]},
        config=config,
        context=context
    )

    structured = response["structured_response"]

    return JsonResponse({
        "punny_response": structured.punny_response,
        "weather_conditions": structured.weather_conditions,
        "session_id": str(session.session_id)
    })
