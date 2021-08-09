from django.contrib.auth.models import User
from rest_framework import serializers


class UserDetailSerializer(serializers.ModelSerializer):
    """ UserDetailSerializer """
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "last_login",
            "date_joined"
        ]
