from rest_framework import serializers
from .models import Article
from user_info.serializers import UserDetailSerializer


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    """ ArticleSerializer """
    author = UserDetailSerializer(read_only=True)

    class Meta:
        model = Article
        fields = "__all__"
