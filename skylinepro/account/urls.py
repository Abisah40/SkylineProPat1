from django.urls import path
from .views import RegisterView,LoginView,ForgetPasswordRequestAPIView,OTPVerificationAPIView,PasswordResetAPIView



    #we use as_view() because the class is a genericAPIView that uses generics.genericAPIView
urlpatterns = [
    path('register-user/', RegisterView.as_view(), name='register-user'),
    path('login-user/', LoginView.as_view(), name= 'login-user'),
    path('forget-password/',ForgetPasswordRequestAPIView.as_view(), name= 'forget-password'),
    path('verify-otp/',OTPVerificationAPIView.as_view(), name= 'verify-otp'),
    path('reset-password/',PasswordResetAPIView.as_view(), name= 'reset-password'),
]