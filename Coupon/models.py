from django.db import models

class Coupon(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.IntegerField()
    companyName = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    isAvailed = models.BooleanField(default=False)
    validityDate = models.DateField()
    directUpload = models.BooleanField(default=True)
    couponCode = models.CharField(max_length=255)
    screenshots = models.ImageField(upload_to='coupon_screenshots/', null=True, blank=True)

class UserProfile(models.Model):
    userId = models.IntegerField(primary_key=True)
    userName = models.CharField(max_length=255)
    userImage = models.ImageField(upload_to='user_profile_images/', null=True, blank=True)
    availedCoupons = models.ManyToManyField(Coupon, related_name='availed_coupons', blank=True)
    uploadedCoupons = models.ManyToManyField(Coupon, related_name='uploaded_coupons', blank=True)
