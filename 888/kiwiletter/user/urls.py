from django.urls import path, include
import user.views as views

urlpatterns = [
    path('google/callback/', views.google_callback, name='google_callback'),
]