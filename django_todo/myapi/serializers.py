from rest_framework import serializers
from todoapp. models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from todoapp import *

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class UserTokenSerializer(TokenObtainPairSerializer):
        @classmethod
        def get_token(cls,user):
            if user is not None and UserProfile.objects.filter(user=user).exists():
                token =super(UserTokenSerializer, cls).get_token(user)
                token['username']=user.username
                return token 