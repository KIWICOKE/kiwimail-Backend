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


BASE_URI = 'http://kiwicoke.com:8000/'
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

    # 1. 받은 코드로 구글에 액세스 토큰 요청
    token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")

    # 1-1. json으로 변환 & 에러 부분 파싱
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    # 1-2. 에러 발생시 종료
    if error is not None:
        raise JSONDecodeError

    # 1-3. 성공시 액세스 토큰 가져오기
    access_token = token_req_json.get('access_token')


    # 2. 가져온 액세스 토큰으로 이메일 값을 구글에 요청
    email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code

    # 2-1. 에러 발생시 400 에러 반환
    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)

    # 2-2. 성공시 이메일 가져오기
    email_req_json = email_req.json()
    email = email_req_json.get('email')

    # 3. 세션에 로그인 정보 저장
    request.session['email'] = email

    return total_auth(email)

def total_auth(request):
    # 세션에서 이메일 정보 가져오기
    email = request.session.get('email', None)
    if email:
        try:
            userCheck = user.objects.get(email = email) #user라는 모델속, 전달받은 email값이 이미 존재하는지 확인한다

            return HttpResponse('existing')

        except user.DoesNotExist: #user가 존재하지 않는다면, user라는 모델속에 새 email을 등록한다.
            emailRegistration = user.objects.create(email = email)
            return HttpResponse('created new')

def main(request):
    return HttpResponse("Welcome")

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
        return HttpResponse(status=200)
        


