from .models import *
from rest_framework import serializers


class ARPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'categoryType', 'dateCreation',  'postCategory', 'title', 'text']


class NWPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'categoryType', 'dateCreation',  'postCategory', 'title', 'text', ]

