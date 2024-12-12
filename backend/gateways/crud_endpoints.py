from flask_sqlalchemy import SQLAlchemy

class BaseGateway:
    """Base Gateway class to handle common operations for models."""
    
    def __init__(self, db: SQLAlchemy, model):
        """
        Initialize the gateway with a database session and a model.
        
        :param db: SQLAlchemy instance
        :param model: SQLAlchemy model class
        """
        self.db = db
        self.model = model

    def get_by_id_filter_fields(self, record_id, fields):
        """
        Fetch a record by ID and return only the specified fields.
        
        :param record_id: The ID of the record to fetch.
        :param fields: List of field names to return in the response.
        :return: Dictionary of the requested fields and their values, or None if the record does not exist.
        """
        try:
            # Fetch the record by ID
            record = self.model.query.get(record_id)
            if not record:
                return None

            # Dynamically filter and return the specified fields
            result = {field: getattr(record, field) for field in fields if hasattr(record, field)}
            return result
        except Exception as e:
            raise Exception(f"Error fetching record with filtered fields: {e}")

    def get_all(self):
        """Fetch all records from the table."""
        try:
            records = self.model.query.all()
            return [record.to_dict() for record in records]
        except Exception as e:
            raise Exception(f"Error fetching records: {e}")

    def get_by_id(self, record_id):
        """Fetch a record by its ID."""
        try:
            record = self.model.query.get(record_id)
            if not record:
                return None
            return record.to_dict()
        except Exception as e:
            raise Exception(f"Error fetching record by ID: {e}")

    def create(self, **kwargs):
        """
        Create a new record dynamically.
        
        :param kwargs: Dictionary of field names and values.
        """
        try:
            valid_fields = {field.name for field in self.model.__table__.columns}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_fields}

            # Check if all required fields are provided
            missing_fields = [
                field.name for field in self.model.__table__.columns
                if not field.nullable and field.default is None and field.name not in filtered_kwargs
            ]
            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            record = self.model(**filtered_kwargs)
            self.db.session.add(record)
            self.db.session.commit()
            return record.to_dict()
        except Exception as e:
            self.db.session.rollback()
            raise Exception(f"Error creating record: {e}")

    def update(self, record_id, **kwargs):
        """
        Update an existing record dynamically.
        
        :param record_id: ID of the record to update.
        :param kwargs: Dictionary of fields to update.
        """
        try:
            record = self.model.query.get(record_id)
            if not record:
                return None

            valid_fields = {field.name for field in self.model.__table__.columns}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_fields}

            for key, value in filtered_kwargs.items():
                setattr(record, key, value)

            self.db.session.commit()
            return record.to_dict()
        except Exception as e:
            self.db.session.rollback()
            raise Exception(f"Error updating record: {e}")

    def delete_by_id(self, record_id):
        """Delete a record by its ID."""
        try:
            record = self.model.query.get(record_id)
            if not record:
                return None
            self.db.session.delete(record)
            self.db.session.commit()
            return {"message": "Record deleted successfully"}
        except Exception as e:
            self.db.session.rollback()
            raise Exception(f"Error deleting record: {e}")
