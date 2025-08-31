import pytest
from datetime import datetime
from uuid import uuid4

from siigo_connector.resources.customers import (
    IdType,
    FiscalResponsibility,
    City,
    Address,
    Phone,
    Contact,
    Metadata,
    Customer,
)


class TestIdType:
    """Test cases for the IdType model."""

    def test_id_type_creation(self):
        """Test IdType creation with valid data."""
        id_type = IdType(code="13", name="Cédula de Ciudadanía")

        assert id_type.code == "13"
        assert id_type.name == "Cédula de Ciudadanía"

    def test_id_type_validation(self):
        """Test that IdType requires both code and name."""
        with pytest.raises(Exception):  # Pydantic validation error
            IdType(code="13")  # Missing name

        with pytest.raises(Exception):  # Pydantic validation error
            IdType(name="Cédula de Ciudadanía")  # Missing code


class TestFiscalResponsibility:
    """Test cases for the FiscalResponsibility model."""

    def test_fiscal_responsibility_creation(self):
        """Test FiscalResponsibility creation with valid data."""
        fiscal_resp = FiscalResponsibility(code="O-23", name="IVA Régimen Común")

        assert fiscal_resp.code == "O-23"
        assert fiscal_resp.name == "IVA Régimen Común"


class TestCity:
    """Test cases for the City model."""

    def test_city_creation_with_all_fields(self):
        """Test City creation with all fields."""
        city = City(
            country_code="CO",
            country_name="Colombia",
            state_code=11,
            state_name="Bogotá D.C.",
            city_code="11001",
            city_name="Bogotá",
        )

        assert city.country_code == "CO"
        assert city.country_name == "Colombia"
        assert city.state_code == 11
        assert city.state_name == "Bogotá D.C."
        assert city.city_code == "11001"
        assert city.city_name == "Bogotá"

    def test_city_creation_with_minimal_fields(self):
        """Test City creation with minimal fields."""
        city = City()

        assert city.country_code is None
        assert city.country_name is None
        assert city.state_code is None
        assert city.state_name is None
        assert city.city_code is None
        assert city.city_name is None


class TestAddress:
    """Test cases for the Address model."""

    def test_address_creation(self):
        """Test Address creation with valid data."""
        city = City(city_name="Bogotá")
        address = Address(address="123 Test Street", city=city, postal_code="12345")

        assert address.address == "123 Test Street"
        assert address.city == city
        assert address.postal_code == "12345"

    def test_address_creation_without_postal_code(self):
        """Test Address creation without postal code."""
        city = City(city_name="Bogotá")
        address = Address(address="123 Test Street", city=city)

        assert address.address == "123 Test Street"
        assert address.city == city
        assert address.postal_code is None


class TestPhone:
    """Test cases for the Phone model."""

    def test_phone_creation_with_all_fields(self):
        """Test Phone creation with all fields."""
        phone = Phone(indicative="57", number="123456789", extension="123")

        assert phone.indicative == "57"
        assert phone.number == "123456789"
        assert phone.extension == "123"

    def test_phone_creation_with_minimal_fields(self):
        """Test Phone creation with minimal fields."""
        phone = Phone()

        assert phone.indicative is None
        assert phone.number is None
        assert phone.extension is None


class TestContact:
    """Test cases for the Contact model."""

    def test_contact_creation_with_phone(self):
        """Test Contact creation with phone."""
        phone = Phone(indicative="57", number="123456789")
        contact = Contact(
            first_name="John", last_name="Doe", email="john.doe@test.com", phone=phone
        )

        assert contact.first_name == "John"
        assert contact.last_name == "Doe"
        assert contact.email == "john.doe@test.com"
        assert contact.phone == phone

    def test_contact_creation_without_phone(self):
        """Test Contact creation without phone."""
        contact = Contact(first_name="John", last_name="Doe", email="john.doe@test.com")

        assert contact.first_name == "John"
        assert contact.last_name == "Doe"
        assert contact.email == "john.doe@test.com"
        assert contact.phone is None


class TestMetadata:
    """Test cases for the Metadata model."""

    def test_metadata_creation(self):
        """Test Metadata creation with valid data."""
        created_time = datetime.now()
        metadata = Metadata(created=created_time)

        assert metadata.created == created_time

    def test_metadata_creation_with_string_date(self):
        """Test Metadata creation with string date."""
        metadata = Metadata(created="2024-01-01T00:00:00Z")

        assert isinstance(metadata.created, datetime)


class TestCustomer:
    """Test cases for the Customer model."""

    def test_customer_creation_minimal(self):
        """Test Customer creation with minimal required fields."""
        customer = Customer(
            id=str(uuid4()),
            type="Customer",
            person_type="Company",
            id_type=IdType(code="13", name="Cédula de Ciudadanía"),
            identification="123456789",
            branch_office=0,
            active=True,
            vat_responsible=False,
        )

        assert customer.type == "Customer"
        assert customer.person_type == "Company"
        assert customer.identification == "123456789"
        assert customer.branch_office == 0
        assert customer.active is True
        assert customer.vat_responsible is False
        assert customer.fiscal_responsibilities == []
        assert customer.phones == []
        assert customer.contacts == []

    def test_customer_creation_full(self, mock_customer_data):
        """Test Customer creation with all fields."""
        customer = Customer(**mock_customer_data)

        assert customer.type == "Customer"
        assert customer.person_type == "Company"
        assert customer.identification == "123456789"
        assert customer.branch_office == 0
        assert customer.check_digit == "1"
        assert customer.name == ["Test Company"]
        assert customer.commercial_name == "Test Co"
        assert customer.active is True
        assert customer.vat_responsible is True
        assert len(customer.fiscal_responsibilities) == 1
        assert customer.address is not None
        assert len(customer.phones) == 1
        assert len(customer.contacts) == 1
        assert customer.comments == "Test customer"
        assert customer.metadata is not None

    def test_customer_with_uuid_id(self):
        """Test Customer creation with UUID id."""
        customer_id = uuid4()
        customer = Customer(
            id=customer_id,
            type="Customer",
            person_type="Company",
            id_type=IdType(code="13", name="Cédula de Ciudadanía"),
            identification="123456789",
            branch_office=0,
            active=True,
            vat_responsible=False,
        )

        assert customer.id == customer_id

    def test_customer_with_string_id(self):
        """Test Customer creation with string id."""
        customer = Customer(
            id="test-id-123",
            type="Customer",
            person_type="Company",
            id_type=IdType(code="13", name="Cédula de Ciudadanía"),
            identification="123456789",
            branch_office=0,
            active=True,
            vat_responsible=False,
        )

        assert customer.id == "test-id-123"

    def test_customer_extra_fields_ignored(self):
        """Test that Customer ignores unexpected fields."""
        customer_data = {
            "id": str(uuid4()),
            "type": "Customer",
            "person_type": "Company",
            "id_type": {"code": "13", "name": "Cédula de Ciudadanía"},
            "identification": "123456789",
            "branch_office": 0,
            "active": True,
            "vat_responsible": False,
            "extra_field": "should_be_ignored",
            "another_extra": 123,
        }

        customer = Customer(**customer_data)

        # Should not raise an error and should not have extra fields
        assert not hasattr(customer, "extra_field")
        assert not hasattr(customer, "another_extra")

    def test_customer_validation_required_fields(self):
        """Test that Customer requires all mandatory fields."""
        # Missing required fields
        with pytest.raises(Exception):  # Pydantic validation error
            Customer(
                id=str(uuid4()),
                type="Customer",
                # Missing person_type
                id_type=IdType(code="13", name="Cédula de Ciudadanía"),
                identification="123456789",
                branch_office=0,
                active=True,
                vat_responsible=False,
            )

    def test_customer_fiscal_responsibilities(self):
        """Test Customer with fiscal responsibilities."""
        fiscal_resp = FiscalResponsibility(code="O-23", name="IVA Régimen Común")
        customer = Customer(
            id=str(uuid4()),
            type="Customer",
            person_type="Company",
            id_type=IdType(code="13", name="Cédula de Ciudadanía"),
            identification="123456789",
            branch_office=0,
            active=True,
            vat_responsible=True,
            fiscal_responsibilities=[fiscal_resp],
        )

        assert len(customer.fiscal_responsibilities) == 1
        assert customer.fiscal_responsibilities[0].code == "O-23"
        assert customer.fiscal_responsibilities[0].name == "IVA Régimen Común"

    def test_customer_phones(self):
        """Test Customer with phones."""
        phone = Phone(indicative="57", number="123456789")
        customer = Customer(
            id=str(uuid4()),
            type="Customer",
            person_type="Company",
            id_type=IdType(code="13", name="Cédula de Ciudadanía"),
            identification="123456789",
            branch_office=0,
            active=True,
            vat_responsible=False,
            phones=[phone],
        )

        assert len(customer.phones) == 1
        assert customer.phones[0].indicative == "57"
        assert customer.phones[0].number == "123456789"

    def test_customer_contacts(self):
        """Test Customer with contacts."""
        contact = Contact(first_name="John", last_name="Doe", email="john.doe@test.com")
        customer = Customer(
            id=str(uuid4()),
            type="Customer",
            person_type="Company",
            id_type=IdType(code="13", name="Cédula de Ciudadanía"),
            identification="123456789",
            branch_office=0,
            active=True,
            vat_responsible=False,
            contacts=[contact],
        )

        assert len(customer.contacts) == 1
        assert customer.contacts[0].first_name == "John"
        assert customer.contacts[0].last_name == "Doe"
        assert customer.contacts[0].email == "john.doe@test.com"
