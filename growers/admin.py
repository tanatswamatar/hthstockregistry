from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import FieldOfficer, Grower, InventoryItem, Allocation

@admin.register(FieldOfficer)
class FieldOfficerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Grower)
class GrowerAdmin(admin.ModelAdmin):
    list_display = ('grower_no', 'surname', 'first_name', 'farm', 'area', 'field_officer')
    search_fields = ('grower_no', 'surname', 'id_number', 'farm')
    list_filter = ('area', 'field_officer')

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_measure', 'unit_price', 'current_stock')
    search_fields = ('name',)

@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = ('grower', 'item', 'quantity', 'delivery_note_no', 'date_issued')
    list_filter = ('item', 'date_issued')
    search_fields = ('grower__grower_no', 'delivery_note_no')
