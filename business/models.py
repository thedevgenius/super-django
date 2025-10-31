from django.db import models
from django.utils.text import slugify
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    level = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Highlight category on home page or top sections.")
    icon = models.ImageField(upload_to='category_icons/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.parent:
            self.level = self.parent.level + 1
        else:
            self.level = 0

        if not self.slug:
            self.slug = slugify(self.name)

        
        super().save(*args, **kwargs)


# class Location(models.Model):
#     name = models.CharField(max_length=255)
#     slug = models.SlugField(unique=True, blank=True, null=True)
    
#     def __str__(self):
#         return self.name


class Business(models.Model):
    # Basic Info
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='businesses')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    tagline = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    # Category and Type
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='businesses')
    subcategory = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='sub_businesses')
    tags = models.JSONField(default=list, blank=True)   # e.g. ["salon", "unisex", "bridal makeup"]

    # Contact & Location
    phone_number = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    address = models.TextField(null=True, blank=True)
    geohash = models.CharField(max_length=12, blank=True, null=True)  # For location-based searches
    
    # Media
    logo = models.ImageField(upload_to='business/logo/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='business/cover/', blank=True, null=True)
    gallery = models.JSONField(default=list, blank=True)  # list of image URLs
    
    # Business Details
    established_year = models.PositiveIntegerField(blank=True, null=True)
    working_hours = models.JSONField(default=dict, blank=True)  
    # Example: {"Mon-Fri": "9 AM - 8 PM", "Sat": "10 AM - 6 PM", "Sun": "Closed"}
    
    # Features / Services
    services = models.JSONField(default=list, blank=True)
    # Example: [{"name": "Haircut", "price": 250, "duration": "30 mins"}]

    payment_methods = models.JSONField(default=list, blank=True)
    # e.g. ["UPI", "Credit Card", "Cash"]
    
    facilities = models.JSONField(default=list, blank=True)
    # e.g. ["AC", "Parking", "Home Service", "Online Booking"]
    
    # Verification & Status
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    subscription_type = models.CharField(max_length=50, choices=[('free', 'Free'), ('one_time', 'One Time'), ('premium', 'Premium')], default='free')
    
    # Ratings & Analytics
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_reviews = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    leads_count = models.PositiveIntegerField(default=0)
    
    # SEO & Search Boosting
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    keywords = models.JSONField(default=list, blank=True)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
