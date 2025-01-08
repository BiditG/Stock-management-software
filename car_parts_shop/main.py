import gspread
from stock_item import StockItem
import sys
sys.path
import pandas as pd

def load_stock_data_from_google_sheet(creds_path, sheet_name):

    gc = gspread.service_account(filename=creds_path)
    sheet = gc.open(sheet_name).sheet1


    data = sheet.get_all_records()
    df = pd.DataFrame(data)


    stock_items = [
        StockItem(
            stock_code=row['Stock Code'],
            quantity=row['Quantity'],
            price=row['Price'],
            stock_name=row['Stock Name'],
            stock_description=row['Stock Description'],
            brand=row['Brand']
        ) 
        for _, row in df.iterrows()
    ]

    return stock_items

def main():
    creds_path = r"C:\Users\User\Desktop\POP\car_parts_shop\ornate-genre-446307-f2-4c61d25f2546.json"
    sheet_name = "stock_data"

    stock_items = load_stock_data_from_google_sheet(creds_path, sheet_name)


    for item in stock_items:
        print(item)

if __name__ == "__main__":
    main()
