# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class TradeConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Join the user's group
#         self.user = self.scope["user"]
#         self.group_name = f"user_{self.user.id}"
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave the group
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)

#     async def receive(self, text_data):
#         # Handle receiving messages from WebSocket
#         pass

#     async def send_trade_notification(self, event):
#         trade_data = event['trade']

#         # Send the trade data to WebSocket
#         await self.send(text_data=json.dumps({
#             'trade': trade_data
#         }))


# blackbeetle/user/consumers.py
# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class TradeConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.group_name = "trades_group"
        
#         # Add this channel to the trades group
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave the trades group
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         trade_data = json.loads(text_data)
        
#         # Send data to WebSocket client
#         await self.send(text_data=json.dumps({
#             'trade': trade_data
#         }))


# consumers.py

# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class TradeConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.group_name = 'trades'

#         # Join group
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave group
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         # Process the received data
#         # For example, broadcast it to the group
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 'type': 'trade_message',
#                 'trade': data['trade'],  # Assuming you're sending a 'trade' field
#             }
#         )

#     async def trade_message(self, event):
#         trade = event['trade']
#         await self.send(text_data=json.dumps({
#             'trade': trade
#         }))


from channels.generic.websocket import AsyncWebsocketConsumer
import json


class TradeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connected")
        # Join the WebSocket group
        await self.channel_layer.group_add("trades_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print("WebSocket disconnected")
        # Leave the WebSocket group
        await self.channel_layer.group_discard("trades_group", self.channel_name)

    # Receive message from group
    async def send_trade_notification(self, event):
        trade_data = event['trade']  # Use 'trade' key to get serialized data
        print("Received trade data:", trade_data)  # Log the received data for debugging
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "trade": trade_data
        }))

