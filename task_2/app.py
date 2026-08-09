from flask import Flask, render_template, jsonify, request
import json
import os


app = Flask(__name__, template_folder='template')

ORDERS_FILE = 'orders.json'


if not os.path.exists(ORDERS_FILE):
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)






MENU_ITEMS = [
    
    {
        "id": 1,
        "name": "Doro Wat",
        "category": "Ethiopian",
        "type": "Traditional",
        "price": 420,
        "rating": 5,
     
        "image": "/static/images/dorowat.jpg",
        "description": "Spicy Ethiopian chicken stew served with fresh injera."
    },
    {
        "id": 2,
        "name": "Tibs",
        "category": "Ethiopian",
        "type": "Popular",
        "price": 450,
        "rating": 5,
        "image": "/static/images/tibs.jpg",
        "description": "Fried beef cubes with vegetables and Ethiopian spices."
    },
    {
        "id": 3,
        "name": "Kitfo",
        "category": "Ethiopian",
        "type": "Chef Special",
        "price": 480,
        "rating": 5,
        "image": "/static/images/kitfo.jpg",
        "description": "Minced beef mixed with Ethiopian butter and spices."
    },
    {
        "id": 4,
        "name": "Misir Wat",
        "category": "Ethiopian",
        "type": "Vegetarian",
        "price": 280,
        "rating": 4,
        "image": "/static/images/misrwat.jpg",
        "description": "Slow cooked red lentils with traditional berbere sauce."
    },

    # ================= INTERNATIONAL FOOD =================
    {
        "id": 5,
        "name": "Pepperoni Pizza",
        "category": "International",
        "type": "Italian",
        "price": 650,
        "rating": 5,
        "image": "/static/images/peoperonipizza.jpg",
        "description": "Crispy pizza with cheese and premium pepperoni."
    },
    {
        "id": 6,
        "name": "Beef Burger",
        "category": "International",
        "type": "Fast Food",
        "price": 520,
        "rating": 4,
        "image": "/static/images/beefburger.jpg",
        "description": "Juicy beef burger served with fries and cheese."
    },
    {
        "id": 7,
        "name": "Chicken Alfredo",
        "category": "International",
        "type": "Pasta",
        "price": 600,
        "rating": 5,
        "image": "/static/images/chickenalferdo.jpg",
        "description": "Creamy pasta with grilled chicken."
    },

    # ================= DRINKS =================
    {
        "id": 8,
        "name": "Coffee",
        "category": "Drinks",
        "type": "Traditional",
        "price": 90,
        "rating": 5,
        "image": "/static/images/coffee.jpeg",
        "description": "Fresh traditional Ethiopian coffee."
    },
    {
        "id": 9,
        "name": "Tea",
        "category": "Drinks",
        "type": "Traditional",
        "price": 50,
        "rating": 5,
        "image": "/static/images/tea.jpeg",
        "description": "Fresh traditional Ethiopian tea."
    },
    {
        "id": 10,
        "name": "Soft Drinks",
        "category": "Drinks",
        "type": "Fresh",
        "price": 90,
        "rating": 5,
        "image": "/static/images/fruitmoktail.jpg",
        "description": "Refreshing cold soft drinks."
    },
    {
        "id": 11,
        "name": "Fresh Juice",
        "category": "Drinks",
        "type": "Fresh",
        "price": 160,
        "rating": 5,
        "image": "/static/images/freshjuice.jpg",
        "description": "Fresh mango, avocado and mixed juices."
    }

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