from rest_framework import serializers
from .models import User

# 序列化；
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid','telephone','username','email','is_staff','is_active')