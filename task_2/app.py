from flask import Flask, jsonify, render_template
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
