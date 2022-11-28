from django.db import models
from django.utils.safestring import mark_safe
# Create your models here.


# VENDOR CLASS 

class Vendor(models.Model):
    full_name = models.CharField(max_length=180)
    email = models.EmailField(max_length=100)
    mobile = models.CharField(max_length=11)
    address=models.TextField()
    types=models.CharField(max_length=150, null=True)

    class Meta:
        verbose_name_plural = 'Vendor'
    
    def __str__(self):
        return self.full_name


# UNIT CLASS 
class Unit(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Unit'

    def __str__(self):
        return self.title


# CATEGORY CLASS 

class Category(models.Model):
    category_name = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.category_name


# PRODUCT CLASS 

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=150)
    details = models.TextField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)



    class Meta:
        verbose_name_plural = 'Product'

    


    def __str__(self):
        return self.product_name


# PURCHASE CLASS

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.FloatField()
    total_amount = models.FloatField(editable=False)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def unit(self):
        return self.product.unit.title

    class Meta:
        verbose_name_plural = 'Purchase'


    def save(self, *args, **kwargs):
        self.total_amount = self.quantity*self.price
        super(Purchase, self).save(*args, **kwargs)

        #save to inventory 

        inventory = Inventory.objects.filter(product=self.product).order_by('-id').first()

        if inventory:
            totalBal = inventory.total_quantity+self.quantity
        else:
            totalBal = self.quantity
        

        Inventory.objects.create(
            product = self.product,
            Purchase = self,    
            sale=None,
            purchase_quantity=self.quantity,
            sales_quantity=None,
            total_quantity= totalBal

        )


# SALES CLASS

class Sales(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.FloatField()
    total_amount = models.FloatField(editable=False)
    sales_date = models.DateTimeField(auto_now_add=True)

    customer_name = models.CharField("Customer",max_length=50, blank=True)
    customer_mobile = models.CharField("Phone",max_length=11)


    class Meta:
        verbose_name_plural = 'Sales'

    def unit(self):
        return self.product.unit.title

    def save(self, *args, **kwargs):
        self.total_amount = self.quantity*self.price
        super(Sales, self).save(*args, **kwargs)

        #save to inventory 
        inventory = Inventory.objects.filter(product=self.product).order_by('-id').first()

        if inventory:
            totalBal = inventory.total_quantity-self.quantity
        else:
            totalBal = self.quantity
        Inventory.objects.create(
            product = self.product,
            Purchase = None,    
            sale=self,
            purchase_quantity=None,
            sales_quantity=self.quantity,
            total_quantity= totalBal

        )
    

#INVENTORY CLASS 

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, default=0,null=True)
    sale = models.ForeignKey(Sales, on_delete=models.CASCADE, default=0,null=True)
    sales_quantity = models.FloatField(default=0,null=True)
    purchase_quantity = models.FloatField(default=0,null=True)
    total_quantity = models.FloatField()


    class Meta:
        verbose_name_plural = 'Inventory'

    def pur_date(self):
        if self.Purchase:
            return self.Purchase.purchase_date
    
        else:
            return "N/A"

    def sale_date(self):
        if self.sale:
            return self.sale.sales_date
    
        else:
            return "N/A"

    def product_unit(self):
        return self.product.unit.title


    def customer(self):
        if self.sale:
            return self.sale.customer_name
    
        else:
            return "N/A"

    def vendor(self):
        if self.Purchase:
            return self.Purchase.vendor.full_name
        else:
            return "N/A"