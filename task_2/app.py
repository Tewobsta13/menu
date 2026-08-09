from flask import Flask, jsonify, render_template, request
import json


app = Flask(__name__, template_folder="template")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/foods", methods=["GET"])
def get_foods():
    with open("static/data/foodData.json", "r") as file:
        foods = json.load(file)
    return jsonify(foods)



@app.route("/orders", methods=["POST"])
def create_order():
    order = request.get_json()
    with open("static/data/orders.json", "r") as file:
        orders = json.load(file)
    orders.append(order)
    with open("static/data/orders.json", "w") as file:
        json.dump(orders, file, indent = 4)
    return jsonify(order), 201