from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import razorpay
from .models import User, Premium

@api_view(['POST'])
def create_razorpay_order(request):
    try:
        request_id = request.data.get("id")
        premium_selected = Premium.objects.get(id=request_id)

        client = razorpay.Client(auth=('rzp_test_TpsHVKhrkZuIUJ', 'OJzAGp6Vqx8yu2qgeHhz4y3o'))

        order_amount = premium_selected.premium_amount * 100  
        order_currency = 'INR'

        order_params = {
            'amount': order_amount,
            'currency': order_currency,
            'payment_capture': '1',
        }

        razorpay_order = client.order.create(order_params)
        order_id = razorpay_order['id']

        return Response({'order_id': order_id, 'order_amount': order_amount}, status=status.HTTP_201_CREATED)
    
    except Premium.DoesNotExist:
        return Response({'error': 'Invalid premium membership selected.'}, status=status.HTTP_404_NOT_FOUND)

    except razorpay.errors.RazorpayError as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Premium
from .serializers import TransactionSerializer
import razorpay
from datetime import timedelta, date

class TransactionAPIView(APIView):

    def post(self, request):
        try:
            
            userid = request.data.get("user_id")
            premiumid = request.data.get("premium_selected")
            
            user = User.objects.get(id=userid)
            premium_selected = Premium.objects.get(id=premiumid)
            
            data = request.data
            data["user_id"] = user.id

            transaction_serializer = TransactionSerializer(data=data)
            
            if transaction_serializer.is_valid():
                
                rz_client = razorpay.Client(auth=('rzp_test_TpsHVKhrkZuIUJ', 'OJzAGp6Vqx8yu2qgeHhz4y3o'))

                try:
                    rz_client.utility.verify_payment_signature({
                        'razorpay_order_id': transaction_serializer.validated_data.get("order_id"),
                        'razorpay_payment_id': transaction_serializer.validated_data.get("payment_id"),
                        'razorpay_signature': transaction_serializer.validated_data.get("signature"),
                    })

                    
                    transaction_serializer.save()

                    
                    if premium_selected.premium_period == 'quarterly':
                        user.premium_validity = date.today() + timedelta(days=90)  
                    elif premium_selected.premium_period == 'monthly':
                        user.premium_validity = date.today() + timedelta(days=30)  
                    
                    user.is_premium_member = True
                    user.premium_details = f"{premium_selected.premium_period.capitalize()} Membership"
                    user.save()

                    response = {
                        "status_code": status.HTTP_201_CREATED,
                        "message": "Transaction created and user upgraded to premium."
                    }
                    return Response(response, status=status.HTTP_201_CREATED)

                except razorpay.errors.SignatureVerificationError as e:
                    return Response({
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "message": "Invalid payment signature.",
                        "error": str(e)
                    }, status=status.HTTP_400_BAD_REQUEST)

            else:
                
                return Response({
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Invalid data.",
                    "error": transaction_serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        except Premium.DoesNotExist:
            return Response({"error": "Invalid premium membership."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
