import hmac
import hashlib
import time
import random
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from adminside.models import Trade
from adminside.serializers import TradeListSerializer


SECRET_KEY = settings.SECRET_KEY

def generate_otp():
    """Generate a 6-digit OTP."""
    return random.randint(1000, 9999)

def generate_hmac(phone_number, otp, expiry_timestamp):

    """Generate HMAC using phone number, OTP, and expiry timestamp."""
    message = f'{phone_number}{otp}{expiry_timestamp}'.encode('utf-8')
    
    hmac_hash = hmac.new(SECRET_KEY.encode('utf-8'), message, hashlib.sha256).hexdigest()
    return hmac_hash

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        mobile_number = request.data.get('mobile_number')

        if not mobile_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(mobile_number=mobile_number).exists()

        if not user:
            return Response({"error": "Phone number is not registered. Please sign up first."}, status=status.HTTP_400_BAD_REQUEST)

        # If the phone number is registered, generate OTP

        otp = generate_otp()
        expiry_timestamp = int(time.time()) + 300  # OTP valid for 5 minutes (300 seconds)

        # Generate HMAC hash
        otp_hash = generate_hmac(mobile_number, otp, expiry_timestamp)
    

        # Simulate sending OTP (e.g., print or log it instead of SMS for testing)
        print(f"Sending OTP {otp} to phone number {mobile_number}")

        return Response({
            'hash': otp_hash,
            'expiry': expiry_timestamp,
        }, status=status.HTTP_200_OK)




class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print(request.data)
        mobile_number = request.data.get('mobile_number')
        otp = request.data.get('otp')
        received_hash = request.data.get('hash')
        expiry_timestamp = request.data.get('expiry')

        # if not mobile_number or not otp or not received_hash or not expiry_timestamp:
        if not mobile_number or not otp or not received_hash :
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the expiry timestamp is valid
        current_timestamp = int(time.time())
        if current_timestamp > int(expiry_timestamp):
            return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)

        # Recompute the hash to verify
        computed_hash = generate_hmac(mobile_number, otp, expiry_timestamp)
        # computed_hash = generate_hmac(mobile_number, otp)
        if hmac.compare_digest(computed_hash, received_hash):
            # OTP is valid, create or get the user
            user = User.objects.get(mobile_number=mobile_number)

            # Generate JWT tokens for the user
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Login successful',
                'user_id': user.id,
                'name': user.first_name,
                'mobile_number' : user.mobile_number
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)



class TradeRecommendation(APIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        
        if user.is_authenticated and user.is_premium_active:
            trade = Trade.objects.all()
            serializer = TradeListSerializer(trade, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "You need to be a premium user to view trade recommendations."}, status=status.HTTP_403_FORBIDDEN)
        

