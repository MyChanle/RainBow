from rest_framework import serializers
from .models import Article


class ArticleDetailSerializer(serializers.ModelSerializer):
    """ ArticleDetailSerializer class """
    class Meta:
        model = Article
        fields = "__all__"


class ArticleListSerializer(serializers.ModelSerializer):
    """ ArticleListSerializer class """
    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ['author']