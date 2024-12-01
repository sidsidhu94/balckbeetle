from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    premium_days_remaining = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'mobile_number', 'premium_details',
                  'is_premium_member', 'premium_validity', 'is_active', 'is_staff','premium_days_remaining']


    def get_premium_days_remaining(self, obj):
        return obj.is_premium_days_remaining()