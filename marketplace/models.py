from django.db import models
from django.contrib.auth.models import User

# 1. User Profile to distinguish between Households and Technicians
class UserProfile(models.Model):
    USER_TYPES = (
        ('household', 'Household / Citizen'),
        ('technician', 'Jua Kali Technician'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='household')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True) # Could later be tied to geolocation

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"

# 2. Categories of E-Waste (e.g., Laptops, Mobile Phones, Printers)
class Category(models.Model):
    name = models.CharField(max_length=100)
    base_salvage_rate = models.DecimalField(max_digits=10, decimal_places=2, help_text="Base value in KSH")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# 3. The actual E-Waste Item being listed
class Item(models.Model):
    CONDITION_CHOICES = (
        ('dead', 'Completely Dead / Won\'t Turn On'),
        ('partially_working', 'Partially Working (e.g., broken screen but turns on)'),
        ('working', 'Working but Obsolete'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listed_items')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, help_text="E.g., Broken HP EliteBook Screen")
    description = models.TextField(help_text="Detailed description of the damage and missing parts")
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='dead')
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    
    # The Valuation Algorithm output
    estimated_salvage_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (Ksh {self.estimated_salvage_value})"

    # --- THE VALUATION ALGORITHM ---
    def calculate_value(self):
        if not self.category:
            return 0.00
            
        base_value = float(self.category.base_salvage_rate)
        
        # Apply multipliers based on the condition
        if self.condition == 'working':
            multiplier = 1.0     # 100% of base salvage value
        elif self.condition == 'partially_working':
            multiplier = 0.50    # 50% of base salvage value
        else: # 'dead'
            multiplier = 0.15    # 15% of base value (just scrap materials)
            
        return base_value * multiplier

    # We override the default save method to run our algorithm automatically
    def save(self, *args, **kwargs):
        # Calculate the value and save it to the database field
        self.estimated_salvage_value = self.calculate_value()
        # Now proceed with the normal Django saving process
        super().save(*args, **kwargs)
    CONDITION_CHOICES = (
        ('dead', 'Completely Dead / Won\'t Turn On'),
        ('partially_working', 'Partially Working (e.g., broken screen but turns on)'),
        ('working', 'Working but Obsolete'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listed_items')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, help_text="E.g., Broken HP EliteBook Screen")
    description = models.TextField(help_text="Detailed description of the damage and missing parts")
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='dead')
    
    # This is where your Valuation Algorithm output will be saved!
    estimated_salvage_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (Ksh {self.estimated_salvage_value})"

    claimed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='claimed_items')