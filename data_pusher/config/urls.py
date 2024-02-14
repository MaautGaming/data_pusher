from django.urls import path, include

urlpatterns = [
    path("", include("pusher_app.urls")),
]
