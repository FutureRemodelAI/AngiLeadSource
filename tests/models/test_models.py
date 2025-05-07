import pytest
from src.model.models import Lead
from src.config import db
from app import create_app
from sqlalchemy.exc import IntegrityError
from src.custom_exception import ConflictException


@pytest.fixture
def lead_data():
    return {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "serviceType": "Consulting",
        "zipCode": "12345",
        "projectDescription": "Need help with a project"
    }


@pytest.fixture
def test_lead(db_session, lead_data):
    lead = Lead.create_lead(lead_data)
    yield lead
    db_session.rollback()


class TestLeadModel:

    def test_create_lead_success(self, db_session, lead_data):
        lead = Lead.create_lead(lead_data)
        assert lead.id is not None
        assert lead.email == lead_data["email"]
        db_session.delete(lead)
        db_session.commit()

    def test_create_lead_duplicate_email(self, db_session, test_lead, lead_data):
        lead_data["email"] = test_lead.email
        with pytest.raises(ConflictException):
            Lead.create_lead(lead_data)

    def test_get_all_leads(self, db_session, test_lead):
        leads = Lead.get_all_leads()
        assert isinstance(leads, list)
        assert any(lead["email"] == test_lead.email for lead in leads)

    def test_get_lead_by_id_success(self, test_lead):
        fetched = Lead.get_lead_by_id(test_lead.id)
        assert fetched["email"] == test_lead.email
        assert fetched["firstName"] == test_lead.first_name

    def test_get_lead_by_id_not_found(self):
        result = Lead.get_lead_by_id(999999)
        assert result is None

    def test_update_lead_success(self, db_session, test_lead):
        updated = Lead.update_lead(test_lead.id, {"first_name": "Jane", "zip_code": "54321"})
        assert updated is True
        updated_lead = Lead.query.get(test_lead.id)
        assert updated_lead.first_name == "Jane"
        assert updated_lead.zip_code == "54321"

    def test_update_lead_not_found(self):
        updated = Lead.update_lead(999999, {"first_name": "Ghost"})
        assert updated is None

    def test_delete_lead_success(self, db_session, lead_data):
        lead = Lead.create_lead(lead_data)
        deleted = Lead.delete_lead(lead.id)
        assert deleted is True
        assert Lead.query.get(lead.id) is None

    def test_delete_lead_not_found(self):
        deleted = Lead.delete_lead(999999)
        assert deleted is None
