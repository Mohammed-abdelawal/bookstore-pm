from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Book, Review

UserModel = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = [
            "book",
        ]


class BookSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = "__all__"
