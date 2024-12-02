# views.py
from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Trade,Premium
from .serializers import TradeSerializer,TradeListSerializer,PremiumSerializer,TradeUpdateSerializer,TradeDetailsSerializer
from rest_framework.permissions import AllowAny
from user.views import User
from user.serializers import UserSerializer
from django.shortcuts import get_object_or_404

class TradeCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print(request.data,"dfh testig  the data ..............")
        serializer = TradeSerializer(data=request.data)
        
        if serializer.is_valid():
            trade = serializer.save()
            return Response({
                "message": "Trade created successfully",
                "trade": TradeSerializer(trade).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TradeUpdateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, trade_id):
        trade = get_object_or_404(Trade, id=trade_id)
        serializer = TradeUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.update_trade_history(trade)
            return Response({
                "message": "Trade history updated successfully",
                "trade_id": trade.id,
                "new_history": {
                    "buy": serializer.validated_data['buy'],
                    "target": serializer.validated_data['target'],
                    "sl": serializer.validated_data['sl'],
                }
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TradeDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        trade = Trade.objects.all().order_by('created_at')
        serializer = TradeListSerializer(trade,many=True)
        return Response(serializer.data)
    

    
class TradeDetailedView(APIView):
    permission_classes = [AllowAny]  # Or any other permission class you prefer

    def get(self, request, trade_id):
        trade = get_object_or_404(Trade, id=trade_id)
        serializer = TradeDetailsSerializer(trade)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PremiumCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        
        serializer = PremiumSerializer(data=request.data)
        
        if serializer.is_valid():
            if serializer.instance:
                serializer.save() 
                return Response({'message': 'Premium entry updated successfully.', 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                
                serializer.save()
                return Response({'message': 'Premium entry created successfully.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        
        premiums = Premium.objects.all()
        
       
        serializer = PremiumSerializer(premiums, many=True)
        
        
        return Response({
            'message': 'Premium entries retrieved successfully.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class PremiumEdit(APIView):
    permission_classes = [AllowAny]
    
    def get_object(self, pk):
        try:
            return Premium.objects.get(pk=pk)
        except Premium.DoesNotExist:
            return None
        
    def patch(self, request, pk):
        premium = self.get_object(pk)
        if not premium:
            return Response({'error': 'Premium entry not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PremiumSerializer(premium, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Premium entry updated successfully.', 'data': serializer.data}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        users = User.objects.filter(is_staff = False)
        
        monthly_users = User.objects.filter(is_premium_member=True, premium_details='Monthly')
        quarterly_users = User.objects.filter(is_premium_member=True, premium_details='Quarterly')
        
        serializer = UserSerializer(users, many=True)
        monthly_serializer = UserSerializer(monthly_users, many=True)
        quarterly_serializer = UserSerializer(quarterly_users, many=True)

        return Response( {
                'users':serializer.data,
                'monthly_members': monthly_serializer.data,
                'quarterly_members': quarterly_serializer.data
            },  status=status.HTTP_200_OK)
    

class UserCountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        counts = User.get_user_counts()
        return Response(counts)
    
class TradeStatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        daily_count = Trade().count_trades_daily()
        monthly_count = Trade().count_trades_monthly()
        expired_trades = Trade().get_expired_trades()

        return Response({
            'daily_trade_count': daily_count,
            'monthly_trade_count': monthly_count,
            'expired_trades': expired_trades
        })
    

class LoginAdmin(APIView):
    def post(self,request):
        if request.method =="POST":
            email =request.data['email']
            password = request.data['password']

            User = get_user_model()

            user = User.objects.filter(email = email,is_superuser = True).first()

            if user is None:
                return Response({"message":"not Authorized"})
            
            if not user.check_password(password):
                return Response({"message":"Incorrect Password"})
            
            
            payload = {
                'id': user.id,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes = 60),
                'iat' : datetime.datetime.utcnow()
            }

        secret_key = 'secret'
        algorithm = 'HS256'

        token = jwt.encode(payload, secret_key,algorithm=algorithm)

        response  = Response()

        response.data ={
            'token' : token,
            'message' : "adminlogin",
            
        }
        

        return response
