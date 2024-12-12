
from flask import Blueprint, Flask, request, jsonify
from backend.models import db
from backend.models.client_models import Clients
from backend.gateways.crud_endpoints import BaseGateway

client_gateway = BaseGateway(db, Clients)

clients_bp = Blueprint('clients', __name__)

@clients_bp.route('/all/', methods=['GET'])
def get_clients():
    try:
        records = client_gateway.get_all()
        return jsonify(records), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@clients_bp.route('/', methods=['POST'])
def create_client():
    try:
        data = request.json
        name = data.get('name', '').strip()
        last_name = data.get('last_name', '').strip()
        email = data.get('email', '').strip()
        phone_number = data.get('phone_number', '').strip()
        address = data.get('address', '').strip()
        location_coordinates = data.get('location_coordinates', '').strip()

        if not name or not last_name or not email or not phone_number:
            return jsonify({"error": "Name, Last Name, Email, and Phone Number are required"}), 400

        # Check for duplicates
        if Clients.query.filter_by(email=email).first():
            return jsonify({"error": "Email already exists"}), 400
        if Clients.query.filter_by(phone_number=phone_number).first():
            return jsonify({"error": "Phone number already exists"}), 400

        # Create the record
        record = Clients(name=name, last_name=last_name, email=email, phone_number=phone_number,
                        address=address, location_coordinates=location_coordinates)
        db.session.add(record)
        db.session.commit()
        return jsonify(record.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500