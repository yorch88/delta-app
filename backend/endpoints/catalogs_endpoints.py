from flask import Blueprint, Flask, request, jsonify
from backend.models import db
from backend.models.catalog_models import ServiceType
from backend.gateways.crud_endpoints import BaseGateway

service_gateway = BaseGateway(db, ServiceType)

servicetype_bp = Blueprint('servicetype', __name__)

@servicetype_bp.route('/all/', methods=['GET'])
def get_clients():
    try:
        records = service_gateway.get_all()
        return jsonify(records), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@servicetype_bp.route('/', methods=['POST'])
def create_servicetype():
    try:
        data = request.json
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()

        if not name or not description:
            return jsonify({"error": "Name and Description are required"}), 400

        # Check for duplicates
        if ServiceType.query.filter_by(name=name).first():
            return jsonify({"error": "Name already exists"}), 400

        # Create the record
        record = ServiceType(name=name, description=description, status="A")
        db.session.add(record)
        db.session.commit()
        return jsonify(record.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500