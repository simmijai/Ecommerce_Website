from django.db import models
from django.utils.text import slugify
from django.conf import settings

# -------------------------------
# 1️⃣ CATEGORY MODEL
# -------------------------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# -------------------------------
# 2️⃣ SUBCATEGORY MODEL
# -------------------------------
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='subcategory_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('category', 'name')
        verbose_name_plural = "Subcategories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} → {self.name}"



# -------------------------------
# 3️⃣ PRODUCT MODEL
# -------------------------------
class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    sku = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    brand = models.CharField(max_length=100, blank=True, null=True)
    
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def _str_(self):
        return self.name


# -------------------------------
# 4️⃣ PRODUCT ATTRIBUTE MODEL (Dynamic key-value)
# -------------------------------
class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attributes")
    key = models.CharField(max_length=100)    # e.g., "Material", "Color", "Seater"
    value = models.CharField(max_length=255)  # e.g., "Cotton", "White", "3-Seater"

    def _str_(self):
        return f"{self.product.name} → {self.key}: {self.value}"


# -------------------------------
# 5️⃣ PRODUCT IMAGE MODEL
# -------------------------------
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images/")
    alt_text = models.CharField(max_length=150, blank=True, null=True)
    is_main = models.BooleanField(default=False)

    def _str_(self):
        return f"Image of {self.product.name}"


# -------------------------------
# 6️⃣ VARIANT MODEL (Optional for advanced usage)
# -------------------------------
class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100)       # Example: Color, Material, Seater
    value = models.CharField(max_length=100)      # Example: Red, Wood, 3-Seater
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)

    def _str_(self):
        return f"{self.product.name} - {self.name}: {self.value}"

