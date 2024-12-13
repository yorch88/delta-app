from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

from backend.models import db
from backend.models.client_models import *
from backend.models.client_models import Clients
from backend.models.user_models import Users
from backend.models.catalog_models import ServiceType
# from backend.models.task_models import Tasks
from backend.endpoints.users_endpoints import users_bp
from backend.endpoints.clients_endpoints import clients_bp
from backend.endpoints.catalogs_endpoints import servicetype_bp
from backend.endpoints.tasks_endpoints import servicerequest_bp

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@db/delta-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# CORS configuration
CORS(app, resources={r"/*": {"origins": "http://localhost:5002"}}, supports_credentials=True, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# Create tables
with app.app_context():
    db.create_all()

# Register blueprints
app.register_blueprint(users_bp, url_prefix='/users/')
app.register_blueprint(clients_bp, url_prefix='/clients/')
app.register_blueprint(servicetype_bp, url_prefix='/servicetype/')
app.register_blueprint(servicerequest_bp, url_prefix='/servicerequest/')

@app.route('/')
def health_check():
    return {"status": "ok", "message": "App is running with hot reload enabled!"}

if __name__ == '__main__':
    app.run(debug=True)
