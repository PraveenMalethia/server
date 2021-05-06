from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(unique=True,max_length=255)
    image = models.ImageField(upload_to="category/images",blank=True,null=True)
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

class Brand(models.Model):
    name = models.CharField(unique=True,max_length=255)
    logo = models.ImageField(upload_to="brands/logo",null=True,blank=True)

    class Meta:
        ordering = ["name"]
    def __str__(self):
        return self.name

    @property
    def logoURL(self):
        try:
            url = self.logo.url
        except:
            url = ""
        return url

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=False)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    special_offer = models.BooleanField(default=False)
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    color = models.CharField(max_length=20, blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    description = RichTextField()
    featured_image = models.ImageField(upload_to="product/images")
    image1 = models.ImageField(upload_to="product/images")
    image2 = models.ImageField(upload_to="product/images")
    image3 = models.ImageField(upload_to="product/images")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


    @property
    def off(self):
        if self.discount_price:
            off = int((self.price-self.discount_price)/self.price*100)
            return off
        else:
            return None
    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ""
        return url

    @property
    def imageURL1(self):
        try:
            url = self.featured_image.url
        except:
            url = ""
        return url

    @property
    def imageURL2(self):
        try:
            url = self.featured_image.url
        except:
            url = ""
        return url

    @property
    def imageURL3(self):
        try:
            url = self.featured_image.url
        except:
            url = ""
        return url

    @property
    def PriceTag(self):
        if self.discount_price:
            last_amount = self.discount_price
        else:
            last_amount = self.price
        return int(last_amount)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_orderd = models.DateTimeField(auto_now=True)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    placed = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    on_the_way = models.BooleanField(default=False)
    delivered_from_us = models.BooleanField(default=False)
    delivered_to_user = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date_orderd"]

    def __str__(self):
        return f"Order ID : {self.id}"

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        return self.orderitem_set.count()

    @property
    def orderItems(self):
        orderitems = self.orderitem_set.all()
        return orderitems


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product}"

    def FORMAT(self):
        from django.utils.timesince import timesince

        return timesince(self.date_added)

    @property
    def get_total(self):
        if self.product.discount_price:
            total = self.product.discount_price * self.quantity
        else:
            total = self.product.price * self.quantity
        return total

class VillageOrCity(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    house_no = models.CharField(blank=True, null=True, max_length=10)
    village_or_city = models.ForeignKey(VillageOrCity,on_delete=models.SET_NULL,blank=True,null=True)
    special_instructions = models.TextField(max_length=200)

    class Meta:
        verbose_name_plural = "Shipping Addresses"
    def __str__(self):
        return self.address