# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from adminside.models import Trade, TradeHistory, Analysis, Insight
# from adminside.serializers import TradeListSerializer

# # @receiver(post_save, sender=Trade)
# @receiver(post_save, sender=TradeHistory)
# @receiver(post_save, sender=Analysis)
# @receiver(post_save, sender=Insight)
# @receiver(post_save, sender=Trade)
# def notify_user_of_trade_update(sender, instance, created, **kwargs):
#     # Get the related Trade object
#     if isinstance(instance, Trade):
#         trade = instance
#     else:
#         trade = instance.trade

#     # Serialize the trade data using TradeListSerializer
#     serialized_data = TradeListSerializer(trade).data

#     # Get the user's channel group based on the trade (you can modify the user relationship if needed)
#     channel_layer = get_channel_layer()
#     trades = f"user_{trade.id}"  # Customize this based on user relations, if applicable

#     print(trades,"just testing the trades updated")
#     # Send the serialized data over WebSocket
#     async_to_sync(channel_layer.group_send)(
#         trades,
#         {
#             "type": "send_trade_notification",
#             "trade": serialized_data,
#         }
#     )


from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from adminside.models import Trade
from adminside.serializers import TradeSerializer
from .models import User

@receiver(post_save, sender=Trade)
def notify_user_of_trade_creation(sender, instance, created, **kwargs):

    print("here just for testing purpose")
    if created :
        print("just check the instance")
        # Serialize the trade data
        serialized_data = TradeSerializer(instance).data
        
        # Get the channel layer for sending WebSocket messages
        channel_layer = get_channel_layer()
        
        # Define the user group for WebSocket communication
        trades_group = f"trades_group"  # Adjust this if you want to target specific users
        
        print(trades_group,"wjechwedjhewjdhbjehwd")

        print(serialized_data)
        # Send the serialized trade data over WebSocket using async_to_sync
        async_to_sync(channel_layer.group_send)(
            trades_group,
            {
                "type": "send_trade_notification",
                "trade": serialized_data,
            }
        )
        print("Data sent to WebSocket")



