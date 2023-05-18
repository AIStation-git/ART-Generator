import json
from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'email', 'contact_no']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)

        data['email'] = self.user.email
        data['created_at'] = self.user.created_at
        data['id'] = self.user.id
        token = Token.objects.get(user=self.user)
        token_to_str = str(token)
        token_to_json = json.dumps(token_to_str)
        token_to_load = json.loads(token_to_json)
        data['token'] = token_to_load
        data['message'] = 'sucessfull'
        return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'credit']    



class BuyCreditSerializer(serializers.Serializer):
    num_credits = serializers.IntegerField()

