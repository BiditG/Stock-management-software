from flask import Flask, request, jsonify
import gspread
from stock_item import StockItem
import pandas as pd

app = Flask(__name__)

def load_stock_data():
    creds_path = r"C:\Users\User\Desktop\POP\car_parts_shop\ornate-genre-446307-f2-4c61d25f2546.json"
    sheet_name = "stock_data"
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

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    intent = req.get('queryResult').get('intent').get('displayName')
    params = req.get('queryResult').get('parameters')

    if intent == "CheckStock":
        stock_code = params.get('StockCode')
        stock_items = load_stock_data()
        item = next((i for i in stock_items if i.get_stock_code() == stock_code), None)
        response_text = f"Stock for item {stock_code} is {item.get_quantity()} units." if item else f"Item {stock_code} not found."
    elif intent == "GetPrice":
        stock_code = params.get('StockCode')
        stock_items = load_stock_data()
        item = next((i for i in stock_items if i.get_stock_code() == stock_code), None)
        response_text = f"The price for item {stock_code} is {item.get_price_before_vat()} before VAT." if item else f"Item {stock_code} not found."
    else:
        response_text = "I didn't understand that. Can you try again?"

    return jsonify({'fulfillmentText': response_text})

if __name__ == '__main__':
    app.run(port=5000)
