from django.shortcuts import render
import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
import requests
from json import JSONDecodeError
from .models import user
from rest_framework.parsers import JSONParser
from user.serializers import insta_serializer
from django.views.decorators.csrf import csrf_exempt


BASE_URI = 'http://127.0.0.1:8000/'
GOOGLE_CALLBACK_URI = BASE_URI + 'api/user/google/callback/'
state = os.environ.get("STATE")

def google_login(request):
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = "456503625210-felrh2s9m5ti9ik7q23bhersrrvm86g1.apps.googleusercontent.com"
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id=456503625210-felrh2s9m5ti9ik7q23bhersrrvm86g1.apps.googleusercontent.com&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")

def google_callback(request):
    client_id = "456503625210-felrh2s9m5ti9ik7q23bhersrrvm86g1.apps.googleusercontent.com"
    client_secret = "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"
    code = request.GET.get('code')
    token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError
    access_token = token_req_json.get('access_token')
    email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code
    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    email_req_json = email_req.json()
    email = email_req_json.get('email')
    return total_auth(email)

def total_auth(email):
    try:
        userCheck = user.objects.get(email = email)
        return HttpResponse('existing')

    except user.DoesNotExist:
        emailRegistration = user.objects.create(email = email)
        return HttpResponse('created new')

@csrf_exempt
def insta(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        search_index = data['id']
        obj = user.objects.get(id = search_index)
        
        serializer = insta_serializer(obj, data = data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse("Good")
        return HttpResponse("No")

    if request.method == 'DELETE':

        data = JSONParser().parse(request)
        search_index = data['id']
        obj = user.objects.get(id = search_index)
        obj.insta = None
        obj.save()
        


