from rest_framework import serializers
from .models import *
from .custom_errors import *

class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'password']
    

class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username']

class UserPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['password']

class CreateTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorizationToken
        fields = ['token', 'user']

class UpdateTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorizationToken
        fields = ['active']

class GetUserHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['user', 'score', 'date']

class SaveUserHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['user', 'score']

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hangman
        fields = ['word', 'tablename']

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tablenames
        fields = ['tname', 'byuser']

"""
class HistorySerializer(serializers.Serializer):
    user = serializers.CharField(max_length=50, unique=True)
    score = serializers.IntegerField(default=0)
    date = serializers.DateField(auto_now=True)
"""

