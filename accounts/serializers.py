from .models import Users
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, required= True, validators=[validate_password])
    password2 = serializers.CharField(write_only = True, required = True)
    class Meta:
        model = Users
        fields = ('email', 'password', 'password2', 'username', 'profile_image', 'name', 'nickname', 'birthday')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                "password": "비밀번호가 일치하지 않습니다."
            })
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  
        return Users.objects.create_user(**validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'username', 'profile_image']
        
    def get_profile_image(self, pic):
        request = self.context.get('request')
        if pic.profile_image:
            return request.build_absolute_uri(pic.profile_image.url)
        return None
    