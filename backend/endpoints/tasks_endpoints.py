from flask import Blueprint, Flask, request, jsonify
from backend.models import db
from backend.models.task_models import ServiceRequest
from backend.gateways.crud_endpoints import BaseGateway

servicerequest_gateway = BaseGateway(db, ServiceRequest)

servicerequest_bp = Blueprint('servicerequest', __name__)

@servicerequest_bp.route('/all/', methods=['GET'])
def get_clients():
    try:
        records = servicerequest_gateway.get_all()
        return jsonify(records), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@servicerequest_bp.route('/', methods=['POST'])
def create_servicerequest():
    try:
        data = request.json
        id_servicetype = data.get('id_servicetype', '')
        description = data.get('description', '').strip()
        status = data.get('status', '').strip()
        if not id_servicetype or not description:
            return jsonify({"error": "Service Type and Description are required"}), 400

        # Check for duplicates
        # if ServiceRequest.query.filter_by(name=name).first():
        #     return jsonify({"error": "Name already exists"}), 400

        # Create the record
        record = ServiceRequest(id_servicetype=id_servicetype, description=description, status=status)
        db.session.add(record)
        db.session.commit()
        return jsonify(record.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500