from django.contrib.auth.models import User
from shortener.models import Users as UserModel
from shortener.models import ShortenedUrls
from rest_framework import serializers



class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",) # comma 필수



class UserSerializer(serializers.ModelSerializer):
    user = UserBaseSerializer(read_only=True) # foreign key

    class Meta:
        model = UserModel
        fields = (
            "id",
            "url_count",
            "organization",
            "user"
        )


class UrlListSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True) # foreign key

    class Meta:
        model = ShortenedUrls
        fields = (
            # "id",
            # "nick_name",
            # "prefix",
            # "shortened_url",
            # "creator",
            # "click",
            # "created_via",
            # "expired_at"
            '__all__'
        )