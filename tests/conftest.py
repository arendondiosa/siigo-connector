import pytest
from unittest.mock import Mock, patch
from uuid import uuid4

from siigo_connector.client import Client
from siigo_connector.config import Config
from siigo_connector.auth import SiigoAuth
from siigo_connector.resources.customers import (
    Customer,
)


@pytest.fixture
def mock_config():
    """Create a mock configuration for testing."""
    return Config(
        base_url="https://api.test.siigo.com",
        timeout=30.0,
        username="test_user",
        access_key="test_key",
        partner_id="test_partner",
    )


@pytest.fixture
def mock_auth_response():
    """Mock authentication response from Siigo."""
    return {
        "access_token": "test_token_12345",
        "expires_in": 3600,
        "token_type": "Bearer",
    }


@pytest.fixture
def mock_customer_data():
    """Sample customer data for testing."""
    return {
        "id": str(uuid4()),
        "type": "Customer",
        "person_type": "Company",
        "id_type": {"code": "13", "name": "Cédula de Ciudadanía"},
        "identification": "123456789",
        "branch_office": 0,
        "check_digit": "1",
        "name": ["Test Company"],
        "commercial_name": "Test Co",
        "active": True,
        "vat_responsible": True,
        "fiscal_responsibilities": [{"code": "O-23", "name": "IVA Régimen Común"}],
        "address": {
            "address": "123 Test Street",
            "city": {
                "country_code": "CO",
                "country_name": "Colombia",
                "state_code": 11,
                "state_name": "Bogotá D.C.",
                "city_code": "11001",
                "city_name": "Bogotá",
            },
            "postal_code": "12345",
        },
        "phones": [{"indicative": "57", "number": "123456789", "extension": "123"}],
        "contacts": [
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@test.com",
                "phone": {"indicative": "57", "number": "987654321"},
            }
        ],
        "comments": "Test customer",
        "metadata": {"created": "2024-01-01T00:00:00Z"},
    }


@pytest.fixture
def mock_customers_response(mock_customer_data):
    """Mock customers list response from Siigo."""
    return {"results": [mock_customer_data], "total": 1, "page": 1, "per_page": 10}


@pytest.fixture
def mock_client(mock_config):
    """Create a mock client for testing."""
    with (
        patch("siigo_connector.client.SiigoAuth") as mock_auth_class,
        patch("siigo_connector.client.SyncTransport") as mock_transport_class,
    ):
        mock_auth = Mock(spec=SiigoAuth)
        mock_transport = Mock()
        mock_transport.request.return_value = Mock()

        mock_auth_class.return_value = mock_auth
        mock_transport_class.return_value = mock_transport

        client = Client(
            username="test_user",
            access_key="test_key",
            partner_id="test_partner",
            base_url="https://api.test.siigo.com",
        )

        return client


@pytest.fixture
def sample_customer(mock_customer_data):
    """Create a sample Customer instance for testing."""
    return Customer(**mock_customer_data)
