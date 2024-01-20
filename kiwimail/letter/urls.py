from django.urls import path
from django.views.generic import TemplateView
from letter.views import MessageCreateView, MessageDetailView

app_name = 'letter'

urlpatterns = [
    path('create/', MessageCreateView.as_view(template_name = 'letter/create.html'), name='create'),
    path('list/', TemplateView.as_view(template_name = 'letter/list.html'), name='list'),
    path('detail/', MessageDetailView.as_view(template_name = 'letter/detail.html'), name='detail'),
]
