from unittest.mock import Mock, patch

import pytest

from siigo_connector.client import Client
from siigo_connector.resources.customers import Customer


class TestIntegration:
    """Integration tests for the complete client flow."""

    @patch("siigo_connector.auth.SiigoAuth._fetch")
    @patch("httpx.Client")
    def test_full_customer_list_flow(self, mock_httpx_client, mock_auth_fetch):
        """Test the complete flow from client creation to customer listing."""
        # Mock auth fetch
        mock_auth_fetch.return_value = None

        # Mock httpx client
        mock_client = Mock()
        mock_httpx_client.return_value = mock_client

        # Mock customers response
        mock_customers_response = Mock()
        mock_customers_response.status_code = 200
        mock_customers_response.json.return_value = {
            "results": [
                {
                    "id": "test-customer-1",
                    "type": "Customer",
                    "person_type": "Company",
                    "id_type": {"code": "13", "name": "Cédula de Ciudadanía"},
                    "identification": "123456789",
                    "branch_office": 0,
                    "active": True,
                    "vat_responsible": False,
                },
                {
                    "id": "test-customer-2",
                    "type": "Customer",
                    "person_type": "Person",
                    "id_type": {"code": "13", "name": "Cédula de Ciudadanía"},
                    "identification": "987654321",
                    "branch_office": 0,
                    "active": True,
                    "vat_responsible": False,
                },
            ]
        }

        # Set up the mock to return different responses for different calls
        mock_client.request.return_value = mock_customers_response

        # Create client
        client = Client(
            username="test_user",
            access_key="test_key",
            partner_id="test_partner",
            base_url="https://api.test.siigo.com",
        )

        # Mock the auth token
        client._http.auth._token = "test_token_12345"

        # Get customers
        customers = list(client.customers.list())

        # Verify results
        assert len(customers) == 2
        assert isinstance(customers[0], Customer)
        assert isinstance(customers[1], Customer)
        assert customers[0].id == "test-customer-1"
        assert customers[1].id == "test-customer-2"
        assert customers[0].person_type == "Company"
        assert customers[1].person_type == "Person"

        # Verify the requests were made correctly
        mock_client.request.assert_called_once()  # Customers request

    @patch("siigo_connector.auth.SiigoAuth._fetch")
    @patch("httpx.Client")
    def test_customer_list_with_parameters(self, mock_httpx_client, mock_auth_fetch):
        """Test customer listing with query parameters."""
        # Mock auth fetch
        mock_auth_fetch.return_value = None

        # Mock httpx client
        mock_client = Mock()
        mock_httpx_client.return_value = mock_client

        # Mock customers response
        mock_customers_response = Mock()
        mock_customers_response.status_code = 200
        mock_customers_response.json.return_value = {"results": []}

        # Set up the mock to return different responses for different calls
        mock_client.request.return_value = mock_customers_response

        # Create client
        client = Client(
            username="test_user",
            access_key="test_key",
            partner_id="test_partner",
            base_url="https://api.test.siigo.com",
        )

        # Mock the auth token
        client._http.auth._token = "test_token_12345"

        # Get customers with parameters
        created_start = "2024-01-01T00:00:00Z"
        list(client.customers.list(created_start=created_start))

        # Verify the requests were made correctly
        mock_client.request.assert_called_once()  # Customers request

    @patch("httpx.Client")
    def test_client_close_cleanup(self, mock_httpx_client):
        """Test that client properly closes resources."""
        # Mock httpx client
        mock_client = Mock()
        mock_httpx_client.return_value = mock_client

        # Create client
        client = Client(username="test_user", access_key="test_key", partner_id="test_partner")

        # Close client
        client.close()

        # Verify httpx client was closed
        mock_client.close.assert_called_once()

    @patch("siigo_connector.auth.SiigoAuth._fetch")
    @patch("httpx.Client")
    def test_authentication_flow(self, mock_httpx_client, mock_auth_fetch):
        """Test that authentication is properly handled."""
        # Mock auth fetch
        mock_auth_fetch.return_value = None

        # Mock httpx client
        mock_client = Mock()
        mock_httpx_client.return_value = mock_client

        # Mock customers response
        mock_customers_response = Mock()
        mock_customers_response.status_code = 200
        mock_customers_response.json.return_value = {"results": []}

        # Set up the mock to return different responses for different calls
        mock_client.request.return_value = mock_customers_response

        # Create client
        client = Client(username="test_user", access_key="test_key", partner_id="test_partner")

        # Mock the auth token
        client._http.auth._token = "test_token_12345"

        # Make a request
        list(client.customers.list())

        # Verify auth fetch was called
        mock_auth_fetch.assert_called_once()

    @patch("siigo_connector.auth.SiigoAuth._fetch")
    @patch("httpx.Client")
    def test_error_handling_flow(self, mock_httpx_client, mock_auth_fetch):
        """Test error handling in the complete flow."""
        from siigo_connector.errors import APIResponseError

        # Mock auth fetch
        mock_auth_fetch.return_value = None

        # Mock httpx client
        mock_client = Mock()
        mock_httpx_client.return_value = mock_client

        # Mock customers response with error
        mock_customers_response = Mock()
        mock_customers_response.status_code = 404
        mock_customers_response.text = "Not Found"

        # Set up the mock to return different responses for different calls
        mock_client.request.return_value = mock_customers_response

        # Create client
        client = Client(username="test_user", access_key="test_key", partner_id="test_partner")

        # Mock the auth token
        client._http.auth._token = "test_token_12345"

        # Attempt to get customers - should raise error
        with pytest.raises(APIResponseError) as exc_info:
            list(client.customers.list())

        assert exc_info.value.status == 404
        assert exc_info.value.message == "Not Found"

    @patch("siigo_connector.auth.SiigoAuth._fetch")
    @patch("httpx.Client")
    def test_customer_data_validation(self, mock_httpx_client, mock_auth_fetch):
        """Test that customer data is properly validated."""
        # Mock auth fetch
        mock_auth_fetch.return_value = None

        # Mock httpx client
        mock_client = Mock()
        mock_httpx_client.return_value = mock_client

        # Mock response with invalid customer data
        mock_customers_response = Mock()
        mock_customers_response.status_code = 200
        mock_customers_response.json.return_value = {
            "results": [
                {
                    "id": "test-customer",
                    "type": "Customer",
                    # Missing required fields
                    "person_type": "Company",
                    # Missing id_type, identification, etc.
                }
            ]
        }

        # Set up the mock to return different responses for different calls
        mock_client.request.return_value = mock_customers_response

        # Create client
        client = Client(username="test_user", access_key="test_key", partner_id="test_partner")

        # Mock the auth token
        client._http.auth._token = "test_token_12345"

        # This should raise a validation error
        with pytest.raises(Exception):  # Pydantic validation error
            list(client.customers.list())

    @patch("siigo_connector.auth.SiigoAuth._fetch")
    @patch("httpx.Client")
    def test_multiple_requests_same_client(self, mock_httpx_client, mock_auth_fetch):
        """Test making multiple requests with the same client."""
        # Mock auth fetch
        mock_auth_fetch.return_value = None

        # Mock httpx client
        mock_client = Mock()
        mock_httpx_client.return_value = mock_client

        # Mock responses for multiple requests
        mock_response1 = Mock()
        mock_response1.status_code = 200
        mock_response1.json.return_value = {
            "results": [
                {
                    "id": "customer1",
                    "type": "Customer",
                    "person_type": "Company",
                    "id_type": {"code": "13", "name": "Test"},
                    "identification": "123",
                    "branch_office": 0,
                    "active": True,
                    "vat_responsible": False,
                }
            ]
        }

        mock_response2 = Mock()
        mock_response2.status_code = 200
        mock_response2.json.return_value = {
            "results": [
                {
                    "id": "customer2",
                    "type": "Customer",
                    "person_type": "Person",
                    "id_type": {"code": "13", "name": "Test"},
                    "identification": "456",
                    "branch_office": 0,
                    "active": True,
                    "vat_responsible": False,
                }
            ]
        }

        # Set up the mock to return different responses for different calls
        mock_client.request.side_effect = [mock_response1, mock_response2]

        # Create client
        client = Client(username="test_user", access_key="test_key", partner_id="test_partner")

        # Mock the auth token
        client._http.auth._token = "test_token_12345"

        # Make first request
        customers1 = list(client.customers.list())
        assert len(customers1) == 1
        assert customers1[0].id == "customer1"

        # Make second request
        customers2 = list(client.customers.list())
        assert len(customers2) == 1
        assert customers2[0].id == "customer2"

        # Verify both requests were made
        assert mock_client.request.call_count == 2
