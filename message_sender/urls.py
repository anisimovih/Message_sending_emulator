from django.urls import path
#from .views import *

from . import views

urlpatterns = [
    path('api/', views.SendMessages.as_view(), name='api'),
]
