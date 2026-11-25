from django.db.migrations import serializer
from django.shortcuts import render
# from account.models import User
from .serializers import RegisterSerializer,LoginSerializer,ForgetPasswordRequestSerializer,VerifyOTPSerializer,PasswordResetSerializer
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.views import APIView


# Create your views here.

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": RegisterSerializer(user, context=self.get_serializer_context()).data,
            "message": "User registered successfully."
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
                'user':{
                'email': user.email,
                'phone_number': user.phone_number,
                'first_name': user.first_name,
                'last_name': user.last_name
                },
                'access': str(refresh.access_token),
                'refresh': str(refresh),
        }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# view for forget password request api

class ForgetPasswordRequestAPIView(generics.GenericAPIView):
    serializer_class = ForgetPasswordRequestSerializer
    permission_classes = []

    def post(self, request):
        serializer =ForgetPasswordRequestSerializer(data=request.data)

        if serializer.is_valid():
            return Response(
                {f"success": True,"message": "OTP has being sent to email" },
                status=status.HTTP_200_OK
                )
        return Response(
            {"success":False, "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
            )


# view for OTP verification api

class OTPVerificationAPIView(generics.GenericAPIView):
    serializer_class = VerifyOTPSerializer
    permission_classes = []

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)

        if serializer.is_valid():
            return Response(
                {"success": True, "message": "OTP is verified successfully"},
                status=status.HTTP_200_OK,
                )
        return Response(
            {"success":False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
            )

# view for reset password api

class PasswordResetAPIView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "message": "Password reset successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )