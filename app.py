import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")  

client = MongoClient(os.getenv("MONGO_URI"))
db = client["ticket_bazar"]
users_collection = db["users"]
tickets_collection = db["tickets"]

jwt = JWTManager(app)

limiter = Limiter(get_remote_address, app=app, default_limits=["100 per hour"])

@app.route("/", methods=["GET"])
@limiter.limit("10 per minute") 
def home():
    return jsonify({"message": "Welcome to Secure Ticket Bazar API!"})

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    if users_collection.find_one({"username": data["username"]}):
        return jsonify({"error": "Username already exists"}), 400

    user = {
        "username": data["username"],
        "password": data["password"] 
    }
    users_collection.insert_one(user)
    return jsonify({"message": "User registered successfully!"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = users_collection.find_one({"username": data.get("username")})

    if not user or user["password"] != data.get("password"): 
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=data["username"])
    return jsonify({"access_token": access_token})

@app.route("/add_ticket", methods=["POST"])
@jwt_required()  
def add_ticket():
    data = request.json
    if not data.get("title") or not data.get("price"):
        return jsonify({"error": "Missing required fields"}), 400

    current_user = get_jwt_identity()  

    ticket = {
        "title": data["title"],
        "price": float(data["price"]),
        "seller": current_user,
        "status": "available"
    }
    tickets_collection.insert_one(ticket)
    return jsonify({"message": "Ticket added successfully!"}), 201

@app.route("/tickets", methods=["GET"])
@limiter.limit("5 per second")  
def get_tickets():
    tickets = list(tickets_collection.find({}, {"_id": 0}))
    return jsonify(tickets)

if __name__ == "__main__":
    app.run(debug=True)
