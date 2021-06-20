from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.


class TshirtProperty(models.Model):
    title = models.CharField(max_length=20, null=False, unique=True)
    slug = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Occasion(TshirtProperty):
    pass


class IdealFor(TshirtProperty):
    pass


class NackType(TshirtProperty):
    pass


class Sleeve(TshirtProperty):
    pass


class Brand(TshirtProperty):
    pass


class Color(TshirtProperty):
    pass


class Tshirt(models.Model):
    name = models.CharField(max_length=50, null=False)
    slug = models.CharField(max_length=200, null=False,
                            unique=True, default='')
    description = models.CharField(max_length=800, null=True)
    discount = models.IntegerField(default=0)
    image = models.ImageField(upload_to='upload/images', null=False)
    occasion = models.ForeignKey(Occasion, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    sleeve = models.ForeignKey(Sleeve, on_delete=models.CASCADE)
    nack_type = models.ForeignKey(NackType, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    ideal_for = models.ForeignKey(IdealFor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SizeVariant(models.Model):
    SIZES = (
        ('S', 'SMALL'),
        ('L', 'LARGE'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('M', 'M'),
        ('FREE', 'FREE'),
        ('XS', 'XS'),
        ('XXS', 'XXS'),
        ('3XL', '3XL'),
        ('4XL', '4XL'),
        ('5XL', '5XL'),
        ('6XL', '6XL'),
        ('38', '38'),
        ('41', '41'),
        ('42', '42'),
        ('43', '43'),
    )
    price = models.IntegerField(null=False)
    tshirt = models.ForeignKey(Tshirt, on_delete=models.CASCADE)
    size = models.CharField(choices=SIZES, max_length=5)

    def __str__(self):
        return self.size
    


class Cart(models.Model):
    sizeVariant = models.ForeignKey(SizeVariant, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name


class Order(models.Model):

    orederStatus = (

        ('PENDING', "Pending"),
        ('PLACED', "Placed"),
        ('CANCLED', 'Canceled'),
        ('COMPLETED', 'COMPLETED')

    )
    method = (
        ('COD', "Case On Delivery"),
        ('ONLINE', "Online")
    )

    order_status = models.CharField(max_length=15, choices=orederStatus)
    payment_method = models.CharField(max_length=15, choices=method)
    shipping_address = models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=12, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.IntegerField(null=False)
    date = models.DateTimeField(null=False, auto_now_add=True)

    def __str__(self):
        return self.user.first_name


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    tshirt = models.ForeignKey(Tshirt, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeVariant, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    price = models.IntegerField(null=False)
    date = models.DateTimeField(null=False, auto_now_add=True)


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.DateTimeField(null=False, auto_now_add=True)
    payment_status = models.CharField(max_length=15, default='FAILED')
    payment_id = models.CharField(max_length=60)
    payment_request_id = models.CharField(
        max_length=60, unique=True, null=False)
