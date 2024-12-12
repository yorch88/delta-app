from backend.models import db

class Clients(db.Model):
    """Model representing a Client in the database."""
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone_number = db.Column(db.String(50), nullable=False, unique=True)
    address = db.Column(db.String(100), nullable=True)
    location_coordinates = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'address': self.address,
            'location_coordinates': self.location_coordinates
        }
