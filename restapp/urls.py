
from .views import *
from django.urls import path


urlpatterns = [

    path('abc/', Notes.as_view()),
    path('abc/<str:pk>/', restdetails.as_view()),


]
