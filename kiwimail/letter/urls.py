from django.urls import path
from django.views.generic import TemplateView
from letter.views import MessageCreateListView, MessageDetailView

app_name = 'letter'

urlpatterns = [
    path('', MessageCreateListView.as_view(), name='create_or_list'),
    path('<int:pk>/', MessageDetailView.as_view(template_name='letter/detail.html'), name='detail'),
]
