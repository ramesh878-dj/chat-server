from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from api.models import Testtable, Friends_table, LikeTable
from rest_framework import exceptions

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password'
        ]
        extra_kwargs = {'password' : {'write_only': True, 'required' : True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # Token.objects.create(user=user)
        return user

class AddSomedataSerializer(serializers.ModelSerializer):
    class Meta:
        model= Testtable
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username= serializers.CharField()
    password= serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user']= user
                else:
                    msg = 'Account is diabled'
                    raise exceptions.ValidationError(msg)            
            else:
                msg = 'Unable to login with this credentials'
                raise exceptions.ValidationError(msg)        
        else:
            msg = 'Must provide username and password'
            raise exceptions.ValidationError(msg)
        return data

class AddFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends_table
        fields = [
            'id',
            'requester_id',
            'requester_name',
            'accepter_id',
            'accepter_name',
            'friends_status'
        ]
        depth=1

class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
        ]

class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model=LikeTable
        fields='__all__'