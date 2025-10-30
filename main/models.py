from django.db import models

class ContactEntry(models.Model):
    inquiry_type = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField(max_length=2000)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class RecruitEntry(models.Model):
    desired_position = models.CharField(max_length=100)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20, blank=True)
    work_experience = models.TextField(blank=True)
    message = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
