from django.urls import path
from django.views.generic import TemplateView
from letter.views import MessageCreateListView, MessageDetailView
import uuid

app_name = 'letter'

urlpatterns = [
    path('<uuid:pk>/', MessageCreateListView.as_view(), name='create_or_list'), # pk = user_id
    path('<uuid:post_id>/', MessageDetailView.as_view(template_name='letter/detail.html'), name='detail'),
]
