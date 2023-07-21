from rest_framework import serializers
from news.models import Source, Crypto, Loan, Health, StudentLoan, Sports, General, Science, Business, Technology, \
    Entertainment, HackersHacking, AnonymousHacking
from user.models import Account, ImageUploadTest
from django.contrib.auth.models import User


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = "__all__"


class NewsByTopicSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop("model", None)
        super().__init__(*args, **kwargs)
        
        if self.model:
            self.Meta.model = self.model

    source = SourceSerializer(many=False)

    class Meta:
        model = None
        fields = "__all__"


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class AccountModelSerializer(serializers.ModelSerializer):
    owner = UserModelSerializer(many=False)
    class Meta:
        model = Account
        fields = [ "id", "owner", "first_name", "last_name", "email", "username", "profile_picture"]


class ImageUploadTestSerializer(serializers.ModelSerializer):
    # image_field = serializers.ImageField()
    class Meta:
        model = ImageUploadTest
        fields = ["image_field"]
