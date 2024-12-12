from backend.models import db

class Users(db.Model):
    """Model representing a User in the database."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_user = db.Column(db.String(50), nullable=False)
    user_level = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            'username': self.username,
            'email': self.email,
            'password_user': self.password_user,
            'user_level': self.user_level
        }
