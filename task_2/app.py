from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from itertools import groupby
import json
import os
import secrets

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'brooklyn.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)              
    order_id = db.Column(db.String(20), nullable=False)       
    customer = db.Column(db.String(120), nullable=False)     
    item = db.Column(db.String(120), nullable=False)          
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False, default=0.0)          
    total_price = db.Column(db.Float, nullable=False, default=0.0)    
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))  
    status = db.Column(db.String(30), nullable=False, default="Pending")         

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "customer": self.customer,
            "item": self.item,
            "quantity": self.quantity,
            "price": self.price,
            "total_price": self.total_price,
            "date_time": self.date_time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self.status,
        }
    
with app.app_context():
    db.create_all()

# Helpers
def generate_order_id():
    """Random public order id, e.g. ORD-3F9A2C1B"""
    return "ORD-" + secrets.token_hex(4).upper()


def save_order(data, order_id=None):
    #  {"customer": "John", "items": [{"name": "Pizza", "quantity": 2, "price": 12.5}, ...]}
    order_id = order_id or generate_order_id()
    customer = data.get("customer", "Guest")
    status = data.get("status", "Pending")
    now = datetime.now(timezone.utc)
    items = data.get("items")
    if not items:
        # single-item order shorthand
        items = [{
            "name": data.get("item") or data.get("food") or data.get("name", "Unknown"),
            "quantity": data.get("quantity", 1),
            "price": data.get("price", 0.0),
        }]

    created_rows = []
    for item in items:
        quantity = int(item.get("quantity", 1))
        price = float(item.get("price", 0.0))
        row = Order(
            order_id=order_id,
            customer=customer,
            item=item.get("name") or item.get("item", "Unknown"),
            quantity=quantity,
            price=price,
            total_price=round(quantity * price, 2),
            date_time=now,
            status=status,
        )
        db.session.add(row)
        created_rows.append(row)

    db.session.commit()
    return created_rows


def group_orders(rows):
    #Group flat Order rows into per-order dicts with an items list, for display.
    rows_sorted = sorted(rows, key=lambda r: r.order_id)
    grouped = []
    for order_id, group in groupby(rows_sorted, key=lambda r: r.order_id):
        group = list(group)
        first = group[0]
        grouped.append({
            "order_id": order_id,
            "customer": first.customer,
            "date_time": first.date_time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": first.status,
            "items": [
                {"row_id": g.id, "item": g.item, "quantity": g.quantity,
                 "price": g.price, "total_price": g.total_price}
                for g in group
            ],
            "order_total": round(sum(g.total_price for g in group), 2),
        })
    return grouped

# ROUTES 
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/foods", methods=["GET"])
def get_foods():
    food_file = os.path.join(BASE_DIR, "static", "data", "foodData.json")
    with open(food_file, "r") as file:
        foods = json.load(file)
    return jsonify(foods)


@app.route("/orders", methods=["POST"])
def create_order():
    payload = request.get_json()

    if isinstance(payload, list):
        for order_data in payload:
            save_order(order_data)
    else:
        save_order(payload)

    return jsonify({"message": "Order saved"}), 201


@app.route("/orders", methods=["GET"])
def get_orders():
    rows = Order.query.all()
    return jsonify([r.to_dict() for r in rows])


# ADMIN ROUTES
@app.route("/admin/orders", methods=["GET", "POST","DELETE","PUT"])
def admin_orders():
    # Handle status update (cancel) / delete actions submitted from the page
    if request.method == "POST":
        order_id = request.form.get("order_id")

        if request.method == "PUT" and order_id:
            rows = Order.query.filter_by(order_id=order_id).all()
            for r in rows:
                r.status = "Cancelled"
            db.session.commit()

        elif request.method == "DELETE" and order_id:
            Order.query.filter_by(order_id=order_id).delete()
            db.session.commit()

        return redirect(url_for("admin_orders"))

    rows = Order.query.all()
    orders = group_orders(rows)
    return render_template("admin_orders.html", orders=orders)


@app.route("/admin/add", methods=["GET", "POST"])
def admin_add():
    if request.method == "POST":
        customer = request.form.get("customer", "Guest")
        item_names = request.form.getlist("item[]")
        quantities = request.form.getlist("quantity[]")
        prices = request.form.getlist("price[]")

        items = []
        for name, qty, price in zip(item_names, quantities, prices):
            if not name:
                continue
            items.append({
                "name": name,
                "quantity": int(qty) if qty else 1,
                "price": float(price) if price else 0.0,
            })

        save_order({"customer": customer, "items": items})
        return redirect(url_for("admin_orders"))

    return render_template("admin_add.html")


if __name__ == "__main__":
    app.run(debug=True)