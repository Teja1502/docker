from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Coupon, UserProfile
from .serializers import CouponSerializer, UserProfileSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from datetime import date


# Function to delete expired coupons
def delete_expired_coupons():
    expired_coupons = Coupon.objects.filter(validityDate__lt=date.today())
    expired_coupons.delete()

# Coupon Views

@api_view(['GET', 'POST'])
def coupon_list_create(request):
    
    # Call function to delete expired coupons
    delete_expired_coupons()
    
    if request.method == 'GET':
        coupons = Coupon.objects.all()
        serializer = CouponSerializer(coupons, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CouponSerializer(data=request.data)
        if serializer.is_valid():
            coupon = serializer.save()
            user_profile = UserProfile.objects.get(userId=coupon.userId)
            user_profile.uploadedCoupons.add(coupon)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def coupon_detail(request, id):
    coupon = get_object_or_404(Coupon, id=id)

    if request.method == 'GET':
        serializer = CouponSerializer(coupon)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = CouponSerializer(coupon, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        coupon.delete()
        return Response(status=204)

# User Profile Views

@api_view(['GET', 'POST'])
def user_profile_list(request):
    if request.method == 'GET':
        user_profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(user_profiles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



# Function to delete expired coupons
def delete_expired_coupons():
    expired_coupons = Coupon.objects.filter(validityDate__lt=date.today())
    expired_coupons.delete()

# Function to update isAvailed field when removing coupons from availedCoupons
def update_isavailed_on_remove(user_profile, removed_coupons_ids):
    removed_coupons = Coupon.objects.filter(id__in=removed_coupons_ids)
    removed_coupons.update(isAvailed=False)
    user_profile.availedCoupons.remove(*removed_coupons)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def user_profile_detail(request, userId):
    user_profile = get_object_or_404(UserProfile, userId=userId)

    # Call function to delete expired coupons
    delete_expired_coupons()

    if request.method == 'GET':
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = UserProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Handle the update of availedCoupons and set isAvailed to True
            availed_coupons_data = request.data.get('availedCoupons', [])
            
            # Ensure availed_coupons_data is a list of dictionaries
            if not isinstance(availed_coupons_data, list):
                return Response({'detail': 'availedCoupons must be a list'}, status=status.HTTP_400_BAD_REQUEST)

            availed_coupons_ids = []
            for coupon_data in availed_coupons_data:
                coupon_id = coupon_data.get('id')
                if coupon_id:
                    availed_coupons_ids.append(coupon_id)

            availed_coupons = Coupon.objects.filter(id__in=availed_coupons_ids)
            
            # Update isAvailed field to True
            availed_coupons.update(isAvailed=True)
            
            user_profile.availedCoupons.set(availed_coupons)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Handle the removal of availedCoupons and set isAvailed to False
        removed_coupons_data = request.data.get('availedCoupons', [])

        # Ensure removed_coupons_data is a list of dictionaries
        if not isinstance(removed_coupons_data, list):
            return Response({'detail': 'availedCoupons must be a list'}, status=status.HTTP_400_BAD_REQUEST)

        removed_coupons_ids = []
        for coupon_data in removed_coupons_data:
            coupon_id = coupon_data.get('id')
            if coupon_id:
                removed_coupons_ids.append(coupon_id)

        removed_coupons = Coupon.objects.filter(id__in=removed_coupons_ids)
        
        # Update isAvailed field to False
        removed_coupons.update(isAvailed=False)
        
        user_profile.availedCoupons.remove(*removed_coupons)

        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_coupon_screenshots(request, id):
    coupon = get_object_or_404(Coupon, id=id)
    if coupon.screenshots:
        return Response({'image': coupon.screenshots.url})
    return Response({'detail': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_user_profile_image(request, userId):
    user_profile = get_object_or_404(UserProfile, userId=userId)
    if user_profile.userImage:
        return Response({'image': user_profile.userImage.url})
    return Response({'detail': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
