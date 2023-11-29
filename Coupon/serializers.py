from rest_framework import serializers
from .models import Coupon, UserProfile

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    availedCoupons = CouponSerializer(many=True, read_only=True)
    uploadedCoupons = CouponSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'

