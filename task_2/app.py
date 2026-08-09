from flask import Flask, render_template, jsonify, request
import json
import os


app = Flask(__name__, template_folder='template')

ORDERS_FILE = 'orders.json'


if not os.path.exists(ORDERS_FILE):
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)



MENU_ITEMS = [
    {"id": 1, "name": "Doro Wat", "price": 450, "image": "/static/images/doro.jpg"},
    {"id": 2, "name": "Beef Tibs", "price": 400, "image": "/static/images/tibs.jpg"},
    {"id": 3, "name": "Shiro Tegabino", "price": 200, "image": "/static/images/shiro.jpg"},
    {"id": 4, "name": "Special Kitfo", "price": 500, "image": "/static/images/kitfo.jpg"}
]

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/menu', methods=['GET'])
def get_menu():
    return jsonify(MENU_ITEMS)

# TASK 1: 

@app.route('/api/orders', methods=['POST'])
def save_order():
    data = request.get_json()

    if not data or 'items' not in data or len(data['items']) == 0:
        return jsonify({"success": False, "message": "Cart is empty! Select at least one item."}), 400

    try:
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            orders = json.load(f)

        orders.append(data)

        with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(orders, f, indent=4)

        return jsonify({"success": True, "message": "Order saved successfully!"}), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# TASK 2: 

@app.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            orders = json.load(f)
        return jsonify(orders)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)