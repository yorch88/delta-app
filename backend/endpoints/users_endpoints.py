
from flask import Blueprint, Flask, request, jsonify
from backend.models import db
from backend.models.user_models import Users
from backend.gateways.crud_endpoints import BaseGateway

user_gateway = BaseGateway(db, Users)

users_bp = Blueprint('users', __name__)

@users_bp.route('/all/', methods=['GET'])
def get_users():
    try:
        records = user_gateway.get_all()
        return jsonify(records), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/', methods=['POST'])
def create_user():
    try:
        data = request.json
        name = data.get('name', '').strip()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password_user = data.get('password_user', '').strip()
        user_level = data.get('user_level', '').strip()

        if not name or not username or not email or not password_user or not user_level:
            return jsonify({"error": "Name, User Name, Email, User Level and Password are required"}), 400

        # Check for duplicates
        if Users.query.filter_by(email=email).first():
            return jsonify({"error": "Email already exists"}), 400
        if Users.query.filter_by(username=username).first():
            return jsonify({"error": "Username already exists"}), 400

        # Create the record
        record = Users(name=name, username=username, email=email, password_user=password_user,
                        user_level=user_level)
        db.session.add(record)
        db.session.commit()
        return jsonify(record.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500