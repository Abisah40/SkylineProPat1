from rest_framework import serializers,status
from .models import CustomUserManager,User
from django.contrib.auth import authenticate
from rest_framework.response import Response
# from datetime import datetime,timedelta

import random
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta

#register serializer for user registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        #this are the fields that will be used for user registration
        fields = ('first_name', 'last_name', 'staff_id','phone_number','email', 'password')

        # To validate the data to use in registration
    def create(self, validated_data):
        user = User.objects.create_user( email=validated_data['email'],first_name=validated_data['first_name'],
        last_name=validated_data['last_name'],staff_id=validated_data['staff_id'],phone_number=validated_data['phone_number'],
        password=validated_data['password'])
        return user

#login serializer for user login
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True,style={'input_type': 'password'})

    def validate(self, data):
        email= data.get('email')
        password = data.get('password')
        
        if email and password:
            #To authenticate email and password in order to check if it exist in the db
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('Unable to log in with provided credentials.', code='authorization')
            else:
                data['user'] = user
                return data
        return Response({'error': 'invalid Password.'}, status=status.HTTP_400_BAD_REQUEST)
    

# forget password serializer
class ForgetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(f"user with email does not exist.")

        # Generate OTP and send via email
        user.generate_otp()
        send_mail(
            "password Reset OTP",
            f"Your OTP for password reset is {user.otp}",
            "isah22234@gmail.com",
            [user.email],
            fail_silently=False,
        )
        return value

# To verify OTP
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "user not found"})

        #check if otp is correct and not expired ||  check whether the OTP a client submitted matches the OTP stored for that user system

        if user.otp != data["otp"]:
            raise serializers.ValidationError({"otp":"OTP is not valid."})

        if user.otp_expires_at < now():
            raise serializers.ValidationError({"otp":"OTP has expired"})

        user.otp_verified = True
        user.save()

        return data

#To reset new password

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(email= data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "user not found"})

        # Check if OTP was verified

        if not user.otp_verified:
            raise serializers.ValidationError({"otp": "OTP verification is required"})

        return data

    def save(self, **kwargs):
        user = User.objects.get(email=self.validated_data["email"])
        user.set_password(self.validated_data["new_password"])

        
        user.otp = None # To Clear OTP after a successful reset

        user.otp_verified =False #To Reset the verification status
        user.save()
        return user

