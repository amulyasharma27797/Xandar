# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from Xandar.util import unique_slug_generator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def get_extra_field(table, extra_attributes):
    fields = table.objects.all().values_list('attribute', flat=True)
    extra_fields = [value for value in fields]
    extra_attributes.append(('Other', tuple([(i, i) for i in extra_fields])))
    return extra_attributes

def validate_quantity(value):
    if value not in range(1, 4):
        raise ValidationError(
            _('Product cannot be more than 3 '),
            params={'value': value},
        )


CATEGORY_CHOICES = (
    ('Men', 'Men'),
    ('Women','Women'),
    ('Electronics', 'Electronics'),
)

SUB_CATEGORY_CHOICES = (

    # Electronics
    ('Mobiles', 'Mobiles'),
    ('Mobile_Accessories', 'Mobile Accessories'),
    ('Laptops', 'Laptops'),
    ('Desktop_PC', 'Desktop PC'),
    ('Tablets', 'Tablets'),
    ('Television', 'Television'),
    ('Air_Conditioner', 'Air Conditioner'),
    ('Refrigerator', 'Refrigerator'),
    ('Washing_Machine', 'Washing Machine'),
    ('Kitchen_Appliances', 'Kitchen Appliances'),

    # Men and Women
    ('T_Shirt', 'T-Shirt'),
    ('Jeans', 'Jeans'),
    ('Inner_Wear', 'Inner Wear'),
    ('Western_Wear', 'Western Wear'),
    ('Ethnic_Wear', 'Ethnic Wear'),
    ('Kurti', 'Kurti'),
    ('Footwear', 'Footwear'),
    ('Sunglasses', 'Sunglasses'),

    # Accessories
    ('Backpack', 'Backpack'),
    ('Handbag', 'Handbag'),
    ('Belt', 'Belt'),

)


class Customer(AbstractUser):
    gender = models.BooleanField(default=True)
    phone_number = models.IntegerField(null=True)

    def __str__(self):
        if self.first_name == '':
            return 'No Name Specified'
        else:
            return self.first_name

class ProductCategory(models.Model):
    category = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
#sabme is_active dalega

    
    def __str__(self):
        return self.category
    
    # class Meta:
    #     verbose_name_plural = 'Product Categories'

class ProductSubcategory(models.Model):
    sub_category = models.CharField(max_length=50)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)



    def __str__(self):
        return self.sub_category




class Product(models.Model):
    name = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    description = models.CharField(max_length=255)
    price = models.PositiveIntegerField(blank=False)
    quantity = models.PositiveIntegerField(default=1)
    count = models.PositiveSmallIntegerField(default=0)
    replacement = models.IntegerField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(ProductSubcategory, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self)
        super(Product, self).save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, parent_link=True)
    image = models.FileField(upload_to='product_images/', default='product_images/default.jpg')


class Attribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.CharField(max_length=50)
    value = models.CharField(max_length=50)


class Wishlist(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product.name

    def get_absolute_url(self):
        return reverse('operations:wishlist')

class WishlistItems(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name
# -------------PREVIOUS WORK - WEEK ONE---------------#
class OrderedItems(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)


class DeliveryAddresses(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    receiver_name = models.CharField(max_length=50, blank=False)
    street_address = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, blank=False)
    pincode = models.IntegerField(blank=False)
    state = models.CharField(max_length=50, blank=False)
    phone_number = models.IntegerField(blank=False)


class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    is_ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name


class CartItems(models.Model):
    choices = [(i, str(i)) for i in range(1, 4)]
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_img = models.ForeignKey(ProductImage, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[validate_quantity, ], choices=choices)
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_('unit price'))

    def __str__(self):
        return self.product.name


class Banner(models.Model):
    title = models.CharField(max_length=50, blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    sub_category = models.CharField(choices=SUB_CATEGORY_CHOICES, max_length=20, blank=True)
    is_active = models.BooleanField(default=False)
    image = models.FileField(upload_to='banner_images/', blank=False)

    def __str__(self):
        return self.title


class TopBanner(models.Model):
    title = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=255)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    sub_category = models.CharField(choices=SUB_CATEGORY_CHOICES, max_length=20, blank=True)
    image = models.FileField(upload_to='banner_images/', blank=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    email = models.EmailField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


