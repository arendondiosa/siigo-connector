from datetime import datetime
from typing import Any, Dict, Iterator, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, TypeAdapter

# ID type constants
ID_TYPE_CC = {"code": "13", "name": "CC"}
ID_TYPE_NIT = {"code": "31", "name": "NIT"}


class IdType(BaseModel):
    code: str
    name: str


class FiscalResponsibility(BaseModel):
    code: str
    name: str


class City(BaseModel):
    country_code: Optional[str] = None
    country_name: Optional[str] = None
    state_code: Optional[int] = None
    state_name: Optional[str] = None
    city_code: Optional[str] = None
    city_name: Optional[str] = None


class Address(BaseModel):
    address: str
    city: City
    postal_code: Optional[str] = None


class Phone(BaseModel):
    indicative: Optional[str] = None
    number: Optional[str] = None
    extension: Optional[str] = None


class Contact(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[Phone] = None


class Metadata(BaseModel):
    created: datetime


class Customer(BaseModel):
    model_config = ConfigDict(extra="ignore")  # ignore unexpected keys safely

    id: UUID | str
    type: Literal["Customer"] | str
    person_type: Literal["Person", "Company"] | str
    id_type: IdType
    identification: str
    branch_office: int
    check_digit: Optional[str] = None
    name: Optional[List[Optional[str]]] = None
    commercial_name: Optional[str] = None
    active: bool
    vat_responsible: bool
    fiscal_responsibilities: List[FiscalResponsibility] = []
    address: Optional[Address] = None
    phones: List[Phone] = []
    contacts: List[Contact] = []
    comments: Optional[str] = None
    metadata: Optional[Metadata] = None


class CustomersResource:
    def __init__(self, *, _request, base_url: str):
        self._request = _request
        self._base = f"{base_url}/v1/customers"

    def get_id_type_code(self, id_type: str) -> Optional[str]:
        """
        Get the ID type code dictionary based on the provided id_type string.
        :param id_type: A string representing the type of identification ("CC" or "NIT").
        :return: A dictionary with 'code' and 'name' keys or None if not found.
        """
        if id_type.upper() == "CC":
            return ID_TYPE_CC["code"]
        elif id_type.upper() == "NIT":
            return ID_TYPE_NIT["code"]
        else:
            return None

    def list(self, *, created_start: Optional[str] = None) -> Iterator[Customer]:
        params: Dict[str, Any] = {}

        if created_start:
            params["created_start"] = created_start

        r = self._request("GET", self._base, params=params)
        data = r.json()
        # Siigo's payload structure usually includes "results"
        items = data.get("results") or data.get("data") or []
        customers = TypeAdapter(list[Customer]).validate_python(items)

        yield from customers

    def create(self, customer_data: dict) -> Customer:
        """
        Create a new customer in Siigo.
        :param customer_data: Dictionary with customer fields matching Siigo API.
        :return: Customer instance of the created customer.
        """
        r = self._request("POST", self._base, json=customer_data)
        data = r.json()
        return Customer.model_validate(data)
