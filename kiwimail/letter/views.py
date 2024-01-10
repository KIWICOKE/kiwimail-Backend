# views.py
from django.shortcuts import render
from django.http import HttpResponse
from letter.models import Message

def write(request):  # 편지 작성하기 기능
    if request.method == "POST":
        writer=request.POST['writer']
        receiver=request.POST['receiver']
        content=request.POST['content']
        writing_pad=request.POST['writing_pad']
        new_message=Message(writer=writer, receiver=receiver, content=content, writing_pad=writing_pad)
        new_message.save()
        return HttpResponse("작성 후에는 수정/삭제가 불가능합니다.")
    else:  # 편지목록 불러오기
        messages={'messages':Message.objects.all()}
        return render(request, 'list.html', messages)

def letter(request):  # 편지 확인하기
    user = request.user
    messages=Message.objects.filter(receiver=user).order_by('-created_at')
    return render(request, 'letter.html', {'letters':messages})
