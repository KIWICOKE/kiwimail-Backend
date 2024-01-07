from django.urls import path
from letter import views
from . import views

urlpatterns = [
    path('', views.write, name='write'),
    path('<int:post_id>/', views.letter, name='check'),
]