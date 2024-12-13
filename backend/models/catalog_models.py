from backend.models import db

class ServiceType(db.Model):
    """Model representing Service Types in the database."""
    __tablename__ = 'servicetypes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(1), nullable=False)

    # Back-reference for all associated ServiceRequest instances
    service_requests = db.relationship('ServiceRequest', back_populates='service_type', lazy=True)

    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status
        }
