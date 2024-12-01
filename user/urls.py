# urls.py
from django.urls import path
from .views import LoginView, VerifyOTPView,TradeRecommendation

urlpatterns = [
    path('login/', LoginView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('trade-recommendations/', TradeRecommendation.as_view(), name='trade-recommendations'),
]
