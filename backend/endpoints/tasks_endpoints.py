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
        phone_number = data.get('phone_number', '').strip()
        email = data.get('email', '').strip()
        nickname = data.get('nickname', '').strip()
        if not id_servicetype or not description or not email or not nickname or not phone_number:
            return jsonify({"error": "Nickname, Email, Phone numnber, Service Type and Description are required"}), 400
        record = ServiceRequest(id_servicetype=id_servicetype, description=description, status="A",
                                phone_number=phone_number, email=email, nickname=nickname)
        db.session.add(record)
        db.session.commit()
        return jsonify(record.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500