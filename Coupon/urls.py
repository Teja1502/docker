from django.urls import path
from .views import (
    coupon_list_create,
    coupon_detail,
    user_profile_list,
    user_profile_detail,
    get_coupon_screenshots, 
    get_user_profile_image
)

urlpatterns = [
    path('coupons/', coupon_list_create, name='coupon-list-create'),
    path('coupons/<int:id>/', coupon_detail, name='coupon-detail'),
    path('user-profiles/', user_profile_list, name='user-profile-list'),
    path('user-profile/<int:userId>/', user_profile_detail, name='user-profile-detail'),
    path('coupon-screenshots/<int:id>/', get_coupon_screenshots, name='get_coupon_screenshots'),
    path('user-profile-image/<int:userId>/', get_user_profile_image, name='get_user_profile_image'),
]
