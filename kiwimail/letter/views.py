from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator

from letter.models import Message
from django.views.generic import CreateView, DetailView, ListView
from django.urls import reverse
from letter.forms import MessageCreationForm
from user.models import user
import uuid
from django.views import View

# 편지 작성
# @method_decorator(login_required, 'get')
# @method_decorator(login_required, 'post')
class MessageCreateListView(CreateView):
    model = Message
    # 편지 목록 불러오기
    def get(self, request, *args, **kwargs):
        # GET 요청에 대한 처리 (ListView)
        user_received_messages = Message.objects.filter(receiver=request.user).order_by('-created_at')
        # return render(request, self.template_name, {'messages': user_messages})
        response_data = [{'content': Message.content, 'writer':Message.writer, 'receiver':Message.receiver }
                         for Message in user_received_messages]
        return JsonResponse(response_data, safe=False)

    # 편지 작성하기
    def post(self, request, *args, **kwargs):
        # POST 요청에 대한 처리 (CreateView)
        form = MessageCreationForm(request.POST)
        if form.is_valid():
            temp_message = form.save(commit=False)
            temp_message.writer = request.user # 현재 로그인한 사용자를 편지의 작성자로 설정
            temp_message.post_id=uuid.uuid4()
            temp_message.save() # 편지 저장
            return render(request, self.template_name, {'messages': Message.objects.all()})

        # form이 유효하지 않은 경우
        return render(request, self.template_name, {'form': form})

# 편지 열람
class MessageDetailView(DetailView):
    model = Message
    context_object_name = 'target_message'
    template_name = 'letter/detail.html'
    pk_url_kwarg = 'post_id'


