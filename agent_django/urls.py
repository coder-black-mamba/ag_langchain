urlpatterns = [
    path("session/create/", create_session),
    path("chat/<uuid:session_id>/", chat_view),
]
