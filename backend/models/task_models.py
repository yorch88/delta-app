from backend.models import db
from backend.models.catalog_models import ServiceType

class ServiceRequest(db.Model):
    """Model representing a Service Request in the database."""
    __tablename__ = 'servicerequest'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    id_servicetype = db.Column(db.Integer, db.ForeignKey('servicetypes.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(1), nullable=False)
    # Relationship to access the associated ServiceType object
    service_type = db.relationship('ServiceType', back_populates='service_requests')

    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            "id": self.id,
            "nickname": self.nickname,
            "email": self.email,
            "phone_number": self.phone_number,
            "description": self.description,
            "status": self.status,
            "service_type": self.service_type.to_dict() if self.service_type else None
        }