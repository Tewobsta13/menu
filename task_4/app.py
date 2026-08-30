from flask import Flask, jsonify, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, timedelta
from itertools import groupby
from functools import wraps
import jwt
import json
import os
import secrets

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'brooklyn.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "insa_projec_jwt_secrate_key_hgjhghruhg_dgu"

db = SQLAlchemy(app)

class Admin(db.Model):
    __tablename__ = "admins"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="admin")


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Integer, default=5)
    image = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "type": self.type,
            "price": self.price,
            "rating": self.rating,
            "image": self.image,
            "description": self.description,
        }

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
    # Create default admin if not exists
    if not Admin.query.filter_by(username="admin").first():
        default_admin = Admin(
            username="admin",
            password_hash=generate_password_hash("password123"),
            role="admin"
        )
        db.session.add(default_admin)
        db.session.commit()
    
    # Create initial items from json if db is empty
    if Item.query.count() == 0:
        food_file = os.path.join(BASE_DIR, "static", "data", "foodData.json")
        if os.path.exists(food_file):
            with open(food_file, "r") as f:
                foods = json.load(f)
                for food in foods:
                    new_item = Item(
                        id=food.get("id"),
                        name=food.get("name"),
                        category=food.get("category"),
                        type=food.get("type"),
                        price=food.get("price"),
                        rating=food.get("rating", 5),
                        image=food.get("image"),
                        description=food.get("description")
                    )
                    db.session.add(new_item)
            db.session.commit()

# --- JWT Middleware ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check authorization header
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        
        # Check cookies if not in header
        if not token and "admin_token" in request.cookies:
            token = request.cookies.get("admin_token")
            
        if not token:
            # If requesting HTML and missing token, redirect to login
            if "text/html" in request.headers.get("Accept", ""):
                return redirect(url_for("admin_login_page"))
            return jsonify({"error": "Token is missing!"}), 401
            
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_admin = Admin.query.filter_by(id=data["admin_id"]).first()
            if not current_admin:
                return jsonify({"error": "Invalid token!"}), 401
            if data.get("role") != "admin":
                return jsonify({"error": "Permission denied!"}), 403
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except Exception:
            return jsonify({"error": "Token is invalid!"}), 401
            
        return f(current_admin, *args, **kwargs)
    return decorated

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
            "order_items": [
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
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items]), 200

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    # data can be a list of cart items: [{name, price, quantity}, ...]
    if isinstance(data, list):
        items = [
            {
                "name": item.get("name", "Unknown"),
                "quantity": int(item.get("quantity", 1)),
                "price": float(item.get("price", 0.0)),
            }
            for item in data
        ]
        created = save_order({"customer": "Guest", "items": items})
    else:
        created = save_order(data)

    order_id = created[0].order_id if created else None
    return jsonify({"message": "Order saved", "order_id": order_id}), 201

@app.route("/orders", methods=["GET"])
@token_required
def get_orders(current_admin):
    rows = Order.query.all()
    return jsonify([r.to_dict() for r in rows])

@app.route("/orders/<order_id>", methods=["GET"])
def get_order_by_id(order_id):
    rows = Order.query.filter_by(order_id=order_id).all()
    if not rows:
        return jsonify({"error": "Order not found"}), 404
    orders = group_orders(rows)
    return jsonify(orders[0]), 200


# AUTH ROUTES
@app.route("/admin/login", methods=["GET"])
def admin_login_page():
    return render_template("admin_login.html")

@app.route("/api/admin/login", methods=["POST"])
def api_admin_login():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Missing username or password"}), 400
        
    admin = Admin.query.filter_by(username=data["username"]).first()
    
    if admin and check_password_hash(admin.password_hash, data["password"]):
        token = jwt.encode({
            "admin_id": admin.id,
            "role": admin.role,
            "exp": datetime.now(timezone.utc) + timedelta(hours=12)
        }, app.config["SECRET_KEY"], algorithm="HS256")
        
        return jsonify({"token": token, "message": "Login successful"}), 200
        
    return jsonify({"error": "Invalid username or password"}), 401


# ADMIN ROUTES
@app.route("/admin/orders", methods=["GET", "POST"])
@token_required
def admin_orders(current_admin):
    # Handle cancel / delete actions submitted via HTML forms (fallback)
    if request.method == "POST":
        order_id = request.form.get("order_id")
        action = request.form.get("action")

        if action == "cancel" and order_id:
            rows = Order.query.filter_by(order_id=order_id).all()
            for r in rows:
                r.status = "Cancelled"
            db.session.commit()

        elif action == "delete" and order_id:
            Order.query.filter_by(order_id=order_id).delete()
            db.session.commit()

        return redirect(url_for("admin_orders"))

    rows = Order.query.all()
    orders = group_orders(rows)
    return render_template("admin.html", orders=orders)


@app.route("/admin/foods", methods=["GET"])
@token_required
def admin_foods_page(current_admin):
    items = Item.query.all()
    return render_template("admin_foods.html", items=items)


@app.route("/admin/orders/<order_id>/cancel", methods=["POST"])
@token_required
def admin_cancel_order(current_admin, order_id):
    rows = Order.query.filter_by(order_id=order_id).all()
    if not rows:
        return jsonify({"error": "Order not found"}), 404
    for r in rows:
        r.status = "Cancelled"
    db.session.commit()
    return jsonify({"message": f"Order {order_id} cancelled"})


@app.route("/admin/orders/<order_id>/delete", methods=["POST"])
@token_required
def admin_delete_order(current_admin, order_id):
    count = Order.query.filter_by(order_id=order_id).delete()
    if count == 0:
        return jsonify({"error": "Order not found"}), 404
    db.session.commit()
    return jsonify({"message": f"Order {order_id} deleted"})


@app.route("/api/admin/foods", methods=["POST"])
@token_required
def admin_add_food(current_admin):
    data = request.get_json()
    new_item = Item(
        name=data.get("name"),
        category=data.get("category"),
        type=data.get("type"),
        price=data.get("price", 0.0),
        rating=data.get("rating", 5),
        image=data.get("image", ""),
        description=data.get("description", "")
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Food added successfully", "item": new_item.to_dict()}), 201

@app.route("/api/admin/foods/<int:item_id>", methods=["DELETE"])
@token_required
def admin_delete_food(current_admin, item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Food not found"}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Food deleted successfully"}), 200


@app.route("/admin/add", methods=["GET", "POST"])
@token_required
def admin_add(current_admin):
    if request.method == "POST":
        # Support JSON from admin.js
        if request.is_json:
            data = request.get_json()
            customer = data.get("customer", "Guest")
            item_name = data.get("items", "Unknown")
            quantity = int(data.get("quantity", 1))
            total_price = float(data.get("total_price", 0.0))
            price = round(total_price / quantity, 2) if quantity else 0.0

            items = [{"name": item_name, "quantity": quantity, "price": price}]
            save_order({"customer": customer, "items": items})
            return jsonify({"message": "Order added"}), 201

        # Fallback: support regular form submission
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