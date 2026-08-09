from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__, template_folder='template', static_folder='static')
ORDER_FILE = os.path.join(os.path.dirname(__file__), 'order.json')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order', methods=['POST'])
def handle_order():
    try:
        new_order = request.get_json()
        orders = []
        if os.path.exists(ORDER_FILE):
            with open(ORDER_FILE, 'r') as f:
                try:
                    orders = json.load(f)
                except json.JSONDecodeError:
                    orders = []
        
        orders.append(new_order)
        
        with open(ORDER_FILE, 'w') as f:
            json.dump(orders, f, indent=4)
            
        return jsonify({"message": "Order placed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
