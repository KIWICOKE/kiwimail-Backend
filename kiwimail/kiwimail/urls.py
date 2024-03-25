from django.contrib import admin
from django.urls import path, include
import user
import user.views as views

urlpatterns = [
    path('api/user/', include('allauth.urls')),
    path('api/user/', include('user.urls')),
    path('api/login/', views.google_login, name='google_login'),
    path('api/insta/', views.insta),
    path('api/post/', include('letter.urls'))
]

