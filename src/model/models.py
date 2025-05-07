from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError

from src.config import db
from src.custom_exception import ConflictException


class Lead(db.Model):
    __tablename__ = 'leads'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    service_type = db.Column(db.String(100))
    zip_code = db.Column(db.String(10))
    project_description = db.Column(db.Text)

    @classmethod
    def create_lead(cls, data: dict):
        try:
            lead = cls(
                first_name=data.get("firstName"),
                last_name=data.get("lastName"),
                email=data.get("email"),
                phone=data.get("phone"),
                service_type=data.get("serviceType"),
                zip_code=data.get("zipCode"),
                project_description=data.get("projectDescription")
            )
            db.session.add(lead)
            db.session.commit()
            return lead
        except IntegrityError as e:
            db.session.rollback()
            if 'leads_email_key' in str(e.orig):
                raise ConflictException("Lead with this email already exists")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating lead: {str(e)}")
            return None

    @classmethod
    def get_all_leads(cls):
        try:
            leads = cls.query.all()
            return [{
                "id": lead.id,
                "firstName": lead.first_name,
                "lastName": lead.last_name,
                "email": lead.email,
                "phone": lead.phone,
                "serviceType": lead.service_type,
                "zipCode": lead.zip_code,
                "projectDescription": lead.project_description
            } for lead in leads]
        except SQLAlchemyError as e:
            print(f"Error fetching leads: {str(e)}")
            return []

    @classmethod
    def get_lead_by_id(cls, lead_id):
        try:
            lead = cls.query.get(lead_id)
            if lead:
                return {
                    "id": lead.id,
                    "firstName": lead.first_name,
                    "lastName": lead.last_name,
                    "email": lead.email,
                    "phone": lead.phone,
                    "serviceType": lead.service_type,
                    "zipCode": lead.zip_code,
                    "projectDescription": lead.project_description
                }
            return None
        except SQLAlchemyError as e:
            print(f"Error fetching lead by ID: {str(e)}")
            return None

    @classmethod
    def update_lead(cls, lead_id, data):
        try:
            lead = cls.query.get(lead_id)
            if lead:
                for key, value in data.items():
                    setattr(lead, key, value)
                db.session.commit()
                return True
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating lead: {str(e)}")
            return None

    @classmethod
    def delete_lead(cls, lead_id):
        try:
            lead = cls.query.get(lead_id)
            if lead:
                db.session.delete(lead)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting lead: {str(e)}")
