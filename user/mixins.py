# from django.conf import settings
# from twilio.rest import Client

# class MessageHandler:
#     mobile_number = None
#     otp = None
#     def __init__(self,mobile_number,otp) -> None:
#         self.mobile_number = mobile_number
#         self.otp = otp

#     def send_otp_on_mobile(self):
#         client = Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)

#         message = client.messages.create(
#             body = 'Hi There',
#             from_ = ,
#             to = ''

#         )



# from twilio.rest import Client
# from django.conf import settings

# client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

# def send_otp(mobile_number):
#     verification = client.verify \
#         .services(settings.TWILIO_VERIFY_SERVICE_SID) \
#         .verifications \
#         .create(to=mobile_number, channel='sms')
#     return verification.status  # This will return 'pending' if successful

# def verify_otp(mobile_number, code):
#     verification_check = client.verify \
#         .services(settings.TWILIO_VERIFY_SERVICE_SID) \
#         .verification_checks \
#         .create(to=mobile_number, code=code)
#     return verification_check.status  # Will return 'approved' if correct


# from twilio.rest import Client
from django.conf import settings

# client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

import random




def send_otp(mobile_number, otp):
    print(otp,mobile_number)
    # message = client.messages.create(
    #     body=f"Your OTP code is {otp}",  
    #     from_= +917306392066,  
    #     to=mobile_number
    # )
    # return message.sid  

def verify_otp(entered_otp, actual_otp):
    return entered_otp == actual_otp 