from django.shortcuts import render
import time
from django.http import JsonResponse


# Create your views here.
def send_json(request):
    data = [{'name': 'Peter', 'email': 'peter@example.org'},
            {'name': 'Julia', 'email': 'julia@example.org'}]
    print("message sent")
    time.sleep(5)
    return JsonResponse(data, safe=False)
