from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from letter.models import Message
from django.views.generic import CreateView, DetailView, ListView
from django.urls import reverse
from letter.forms import MessageCreationForm
from user.models import user

# 편지 작성
@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class MessageCreateView(CreateView):
    model = Message
    form_class = MessageCreationForm
    template_name = 'letters/create.html'

    def form_valid(self, form):
        temp_message=form.save(commit=False)
        temp_message.writer=self.request.user
        temp_message.save()
        return super().form_valid(form)

        def get_success_url(self):
            return reverse('letter:list', kwargs={'pk': self.object.pk})

# 편지 열람
class MessageDetailView(DetailView):
    model = Message
    context_object_name = 'target_message'
    template_name = 'letter/detail.html'

class MessageListView(ListView):
    model = user
    context_object_name = 'target_user'
    template_name = 'letter/list.html'
    ordering = ['-created_at']
