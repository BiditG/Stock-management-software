from flask import Flask, render_template, request, jsonify
import gspread
from stock_item import StockItem
import pandas as pd
import logging

app = Flask(__name__)

def load_stock_data():
    try:
        creds_path = r"C:\Users\User\Desktop\POP\car_parts_shop\ornate-genre-446307-f2-ecd51e3298ba.json"
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
    except Exception as e:
        logging.exception("An error occurred while loading stock data.")
        return []

def get_stock_info(stock_code):
    stock_items = load_stock_data()
    if not stock_items:
        return "Unable to load stock data at the moment. Please try again later."
    item = next((i for i in stock_items if i.get_stock_code() == stock_code), None)
    if item:
        return f"Stock for item {stock_code} is {item.get_quantity()} units."
    else:
        return f"Item {stock_code} not found."

def get_price_info(stock_code):
    stock_items = load_stock_data()
    if not stock_items:
        return "Unable to load stock data at the moment. Please try again later."
    item = next((i for i in stock_items if i.get_stock_code() == stock_code), None)
    if item:
        return f"The price for item {stock_code} is {item.get_price_before_vat()} before VAT."
    else:
        return f"Item {stock_code} not found."

def get_description_info(stock_code):
    stock_items = load_stock_data()
    if not stock_items:
        return "Unable to load stock data at the moment. Please try again later."
    item = next((i for i in stock_items if i.get_stock_code() == stock_code), None)
    if item:
        return f"Description for item {stock_code}: {item.get_stock_description()}"
    else:
        return f"Item {stock_code} not found."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api', methods=['POST'])
def api():
    user_input = request.json.get('user_input').strip()
    user_input_parts = user_input.split()

    if len(user_input_parts) < 2:
        response = "Please provide a valid command and stock code. Type 'help' for a list of commands."
    else:
        command = user_input_parts[0].lower()
        stock_code = user_input_parts[1]

        if command == "stock":
            response = get_stock_info(stock_code)
        elif command == "price":
            response = get_price_info(stock_code)
        elif command == "describe":
            response = get_description_info(stock_code)
        else:
            response = "I'm sorry, I didn't understand that. Type 'help' for commands I can understand."

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
