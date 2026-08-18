from flask import Flask, jsonify, render_template, request
import json
import os

app = Flask(__name__, template_folder="template")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/foods", methods=["GET"])
def get_foods():
    food_file = os.path.join(
        BASE_DIR,
        "static",
        "data",
        "foodData.json"
    )

    with open(food_file, "r") as file:
        foods = json.load(file)

    return jsonify(foods),200


@app.route("/orders", methods=["POST"])
def create_order():
    new_order = request.get_json()

    orders_file = os.path.join(
        BASE_DIR,
        "static",
        "data",
        "orders.json"
    )

    with open(orders_file, "r") as file:
        orders = json.load(file)
    if isinstance(new_order, list):
        for order in new_order:
            orders.append(order)
    else:
            orders.append(new_order)
            
    

    with open(orders_file, "w") as file:
        json.dump(orders, file, indent=4)

    return jsonify(new_order), 201


@app.route("/orders", methods=["GET"])
def get_orders():
    orders_file = os.path.join(
        BASE_DIR,
        "static",
        "data",
        "orders.json"
    )

    with open(orders_file, "r") as file:
        orders = json.load(file)

    return jsonify(orders),200

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Route not found"}), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)