from django.urls import path

from .views import *
urlpatterns = [
    path('',HomeView.as_view()),
    path('task/<str:pk>',UpdateTask.as_view(),name="task"),
    path('login',LoginView.as_view())
]
