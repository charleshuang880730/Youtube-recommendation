from django.contrib.auth.models import User, Group
from rest_framework import serializers
from search.models import Charles


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        #fields = ['url', 'username', 'email', 'groups']
        fields = ['url', 'username', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class CharlesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Charles
        fields = ['password']
