from rest_framework import serializers
from .models import user

class insta_serializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['id', 'insta'] 
