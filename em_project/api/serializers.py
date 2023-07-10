from rest_framework import serializers
from .models import CustomUser, Job
from django.contrib.auth import get_user_model

# from django.contrib.auth import authenticate


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            "is_staff",
            "is_active",
            "password",
            "is_superuser",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid username")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password")

        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username"]


class JobSerializer(serializers.ModelSerializer):
    employees = serializers.SlugRelatedField(
        many=True, queryset=get_user_model().objects.all(), slug_field="username"
    )

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "comments",
            "employees",
            "start_date",
            "end_date",
            "status",
            "submission_date",
        ]

    def validate(self, data):
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError(
                "Start date should be less than the end date."
            )

        return data

    def create(self, validated_data):
        employees = validated_data.pop("employees")
        job = Job.objects.create(**validated_data)
        job.employees.set(employees)
        return job
