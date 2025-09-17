from datetime import datetime
from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, TypeAdapter


class Webhook(BaseModel):
    model_config = ConfigDict(extra="ignore")  # ignore unexpected keys safely

    id: Union[UUID, str]
    application_id: str
    url: str
    topic: str
    company_key: str
    active: bool
    created_at: datetime


class WebhookResource:
    def __init__(self, *, _request, base_url: str):
        self._request = _request
        self._base = f"{base_url}/v1/webhooks"
        self.webhook_type_map = {
            "PRODUCTS_CREATE": "public.siigoapi.products.create",
            "PRODUCTS_UPDATE": "public.siigoapi.products.update",
            "STOCK_UPDATE": "public.siigoapi.products.stock.update"
        }

    def list(self) -> List[Webhook]:
        """List webhooks

        Args:
            **params: Optional query parameters to filter the results.

        Returns:
            dict: A dictionary containing the list of webhooks.
        """
        r = self._request("GET", self._base)
        data = r.json()

        return TypeAdapter(List[Webhook]).validate_python(data)

    def get_by_type(self, webhook_type: str) -> Optional[Webhook]:
        r = self._request("GET", self._base)
        data = r.json()

        # Find the webhook with the matching topic
        webhook = next((wh for wh in data if wh["topic"] == self.webhook_type_map[webhook_type]), None)
        return TypeAdapter(Webhook).validate_python(webhook) if webhook else None


    def select(self, webhook_type: str) -> Webhook:
        """Retrieve a specific webhook by its ID.

        Args:
            webhook_id (str): The ID of the webhook to retrieve.

        Returns:
            dict: A dictionary containing the webhook details.
        """

        if webhook_type not in self.webhook_type_map:
            raise ValueError(f"Invalid webhook type: {webhook_type}")

        # Find the webhook with the matching topic
        webhook = self.get_by_type(webhook_type=webhook_type)

        if not webhook:
            raise ValueError(f"Webhook with type {webhook_type} not found")

        return TypeAdapter(Webhook).validate_python(webhook)

    def upsert(self, webhook_type: str, url: str) -> Webhook:
        if webhook_type not in self.webhook_type_map:
            raise ValueError(f"Invalid webhook type: {webhook_type}")

        if not url or not url.startswith("http"):
            raise ValueError("Invalid URL. It must start with 'http://' or 'https://'")

        # Find the webhook with the matching topic
        webhook = self.get_by_type(webhook_type=webhook_type)


    def create(self, webhook_type: str, url: str) -> Webhook:
        if webhook_type not in self.webhook_type_map:
            raise ValueError(f"Invalid webhook type: {webhook_type}")

        if not url or not url.startswith("http"):
            raise ValueError("Invalid URL. It must start with 'http://' or 'https://'")

        payload = {
            "topic": self.webhook_type_map[webhook_type],
            "url": url,
            "active": True
        }

        r = self._request("POST", self._base, json=payload)
        data = r.json()

        return TypeAdapter(Webhook).validate_python(data)

    def delete(self, webhook_id: str) -> None:
        """Delete a specific webhook by its ID.

        Args:
            webhook_id (str): The ID of the webhook to delete.

        Returns:
            None
        """
        r = self._request("DELETE", f"{self._base}/{webhook_id}")
        if r.status_code != 200:
            raise Exception(f"Failed to delete webhook with ID {webhook_id}. Status code: {r.status_code}")

