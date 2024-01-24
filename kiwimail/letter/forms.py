from django.forms import ModelForm
from letter.models import Message

class MessageCreationForm(ModelForm):
    class Meta(object):
        model = Message
        fields = ['writer', 'receiver', 'content']
        # 편지지, 이모티콘, 공개여부
