import os
import django
import pandas as pd
from decimal import Decimal

# 1. Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockregister.settings')
django.setup()

from growers.models import Grower, FieldOfficer, InventoryItem, Allocation

def run_import():
    file_path = 'TANATSWA.xlsm'
    
    # --- Part A & B: Growers & Field Officers ---
    print("Reading Growers sheet...")
    # Loading the sheet
    df_master = pd.read_excel(file_path, sheet_name='growers & fo ')
    
    # CLEANING: Remove spaces from column names and make them uppercase
    df_master.columns = [str(c).strip().upper() for c in df_master.columns]
    
    print(f"Verified Columns: {list(df_master.columns)}")

    print("Importing Field Officers and Growers...")
    for index, row in df_master.iterrows():
        # Get values safely using uppercase keys
        fo_name = str(row.get('FIELD OFFICER', '')).strip()
        g_no = str(row.get('GROWER NUMBER', '')).strip()

        # Skip empty rows
        if g_no == 'nan' or not g_no:
            continue

        # Handle Field Officer
        fo = None
        if fo_name and fo_name != 'nan':
            fo, _ = FieldOfficer.objects.get_or_create(name=fo_name)

        # Handle Grower
        Grower.objects.update_or_create(
            grower_no=g_no,
            defaults={
                'surname': str(row.get('LAST NAME', '')).strip(),
                'first_name': str(row.get('FIRST NAME', '')).strip(),
                'id_number': str(row.get('ID NUMBER', '')).strip(),
                'farm': str(row.get('FARM', ''))[:200].strip(),
                'area': str(row.get('AREA', '')).strip(),
                'phone': str(row.get('PHONE NUMBER', '')).strip(),
                'hectares': Decimal(str(row.get('HECT', '0'))) if not pd.isna(row.get('HECT')) else Decimal('0.00'),
                'field_officer': fo
            }
        )

    # --- Part C: Import Products from 'FINAL' sheet ---
    print("\nIdentifying Inventory Items from 'FINAL'...")
    # In 'FINAL', row 0 and 1 are usually headers/prices. Data starts lower.
    df_final = pd.read_excel(file_path, sheet_name='FINAL ')
    
    # Column mapping logic (every 2nd column starting at index 11)
    product_cols = range(11, 56, 2) 
    item_map = {}
    
    for col in product_cols:
        item_name = str(df_final.columns[col]).strip()
        if "Unnamed" in item_name or not item_name:
            continue
            
        # Price is typically in the row directly below the header or row 0
        price_val = df_final.iloc[0, col+1] 
        if pd.isna(price_val) or not isinstance(price_val, (int, float, Decimal)):
            price_val = 0.0

        item, _ = InventoryItem.objects.update_or_create(
            name=item_name,
            defaults={
                'unit_price': Decimal(str(price_val)),
                'unit_measure': "50KG"
            }
        )
        item_map[col] = item

    # --- Part D: Import Allocations ---
    print("Recording Transactions...")
    # Data rows usually start after the price/header rows
    data_rows = df_final.iloc[2:] 

    for _, row in data_rows.iterrows():
        # Column 0 is Grower Number
        g_no = str(row.iloc[0]).strip()
        if g_no == 'nan' or not g_no:
            continue
        
        try:
            grower = Grower.objects.get(grower_no=g_no)
            # Column 9 is typically Delivery Note
            d_note = str(row.iloc[9]) if not pd.isna(row.iloc[9]) else ""
            
            for col, item in item_map.items():
                qty = row.iloc[col]
                # Only record if there is a quantity
                if qty and not pd.isna(qty) and float(qty) > 0:
                    Allocation.objects.create(
                        grower=grower,
                        item=item,
                        quantity=Decimal(str(qty)),
                        delivery_note_no=d_note
                    )
        except Grower.DoesNotExist:
            print(f"Warning: Grower {g_no} not found in database. Skipping allocation.")
            continue

    print("\nSuccess! Data imported into Stock Register.")

if __name__ == '__main__':
    run_import()