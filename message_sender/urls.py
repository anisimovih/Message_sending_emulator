from django.urls import path
#from .views import *

from . import views

urlpatterns = [
    path('send/', views.send_json, name='send_json'),
]
