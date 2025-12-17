from django.db import models

# Create your models here.


from django.db import models

class FieldOfficer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Grower(models.Model):
    grower_no = models.CharField(max_length=20, unique=True)
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=50)
    farm = models.CharField(max_length=200)
    area = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    hectares = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    field_officer = models.ForeignKey(FieldOfficer, on_delete=models.SET_NULL, null=True, related_name='growers')

    def __str__(self):
        return f"{self.grower_no} - {self.surname}"

class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    unit_measure = models.CharField(max_length=20, default="50KG")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name

from django.db import models, transaction
from django.core.exceptions import ValidationError

class Allocation(models.Model):
    grower = models.ForeignKey(Grower, on_delete=models.CASCADE, related_name='allocations')
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='allocation')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    date_issued = models.DateTimeField(auto_now_add=True)
    delivery_note_no = models.CharField(max_length=50, blank=True)

    @property
    def total_cost(self):
        return self.quantity * self.item.unit_price

    def clean(self):
        """
        Prevents issuing more stock than what is currently in the warehouse.
        """
        if self.item and self.quantity:
            if self.quantity > self.item.current_stock:
                raise ValidationError({
                    'quantity': f"Insufficient stock! Only {self.item.current_stock} {self.item.unit_measure} of {self.item.name} available."
                })

    def save(self, *args, **kwargs):
        """
        Automatically subtracts the quantity from InventoryItem when saved.
        """
        # Ensure the clean() method is called before saving
        self.full_clean()
        
        with transaction.atomic():
            # Only subtract stock if this is a new record (not an edit)
            if not self.pk:
                self.item.current_stock -= self.quantity
                self.item.save()
            
            super().save(*args, **kwargs)
