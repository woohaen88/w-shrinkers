from django.contrib.auth.models import User
from shortener.models import Users as UserModel
from shortener.models import ShortenedUrls
from rest_framework import serializers

from shortener.utils import url_count_changer


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

class UrlCreateSerializer(serializers.Serializer):
    nick_name = serializers.CharField(max_length=50)
    target_url = serializers.CharField(max_length=2000)
    category = serializers.IntegerField(required=False)

    def create(self, request, data, commit=True):
        instance = ShortenedUrls()
        instance.creator_id = request.user.id
        instance.category = data.get("category", None)
        instance.target_url = data.get("target_url").strip()
        if commit:
            try:
                instance.save()
            except Exception as e:
                print(e)
            else:
                url_count_changer(request, True)
        return instance