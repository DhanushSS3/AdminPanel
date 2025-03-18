from rest_framework import serializers
from .models import UserProfile
from .models import Group
from .models import Order
from rest_framework import serializers
from .models import WithdrawalRequest, UserProfile

class UserProfileLimitedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id', 'name', 'email', 'phone_number', 'password', 'wallet_total_amount',
            'status', 'group', 'leverage', 'account_number', 'created_at', 'bank_account_number', 'bank_ifsc_code'
        ]



class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'symbol',
            'name',
            'commision',
            'commision_type',
            'commision_value_type',
            'margin',
            'spread',
            'deviation',
            'min_lot',
            'max_lot',
        ]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'  # Or specify fields: ['id', 'customer_name', ...]



from rest_framework import serializers
from .models import WithdrawalRequest, UserProfile

# New Serializer for Limited User Profile Data
class UserProfileWithdrawalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'email', 'phone_number']

# Existing WithdrawalRequestSerializer (with updated UserProfile usage)
class WithdrawalRequestSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField() #use SerializerMethodField

    class Meta:
        model = WithdrawalRequest
        fields = '__all__'

    def get_user_details(self, obj):
        try:
            user_profile = UserProfile.objects.get(id=obj.user_id)
            return UserProfileWithdrawalRequestSerializer(user_profile).data
        except UserProfile.DoesNotExist:
            return None #or return empty dict, or handle as needed.
