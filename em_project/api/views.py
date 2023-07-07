from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework import status,generics
from .models import CustomUser,Job
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    CustomUserSerializer,
    UserLoginSerializer,
    JobSerializer
)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_data = {
                "message": "User registered successfully",
                "user": serializer.data 
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token = get_tokens_for_user(user)
            return Response(
                {"token": token,
                  "is_manager": user.is_staff,
                "message": "Login successful"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = CustomUser.objects.filter(is_staff=False)
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data)

class JobView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


    def patch(self, request, pk):
        try:
            job = Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            return Response({'detail': 'Job not found.'}, status=404)

        serializer = JobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class AssignedJobsView(APIView):
    def get(self, request):
        employee = request.user 
        jobs = employee.jobs_assigned.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

class JobStatusView(APIView):

    def put(self, request, pk):
        try:
            job = Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            return Response({'detail': 'Job not found.'}, status=status.HTTP_404_NOT_FOUND)


        status_value = request.data.get('status')
        comment = request.data.get('comments')

        data = {
            'status': status_value,
            'comments': comment,
        }
        serializer = JobSerializer(job, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)