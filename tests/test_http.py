from unittest.mock import Mock, patch

import httpx
import pytest

from siigo_connector._http import SyncTransport
from siigo_connector.auth import SiigoAuth
from siigo_connector.config import Config
from siigo_connector.errors import APIConnectionError, APIResponseError, APITimeoutError


class TestSyncTransport:
    """Test cases for the SyncTransport class."""

    def test_sync_transport_initialization(self, mock_config):
        """Test SyncTransport initialization."""
        auth = SiigoAuth(mock_config)
        transport = SyncTransport(mock_config, auth)

        assert transport.cfg == mock_config
        assert transport.auth == auth
        assert transport.client is not None

    def test_sync_transport_close(self, mock_config):
        """Test that close method closes the client."""
        auth = SiigoAuth(mock_config)
        transport = SyncTransport(mock_config, auth)

        # Mock the client close method
        transport.client.close = Mock()

        transport.close()
        transport.client.close.assert_called_once()

    @patch.object(SiigoAuth, "token")
    def test_sync_transport_headers(self, mock_token, mock_config):
        """Test that headers include Partner-Id and Bearer token."""
        mock_token.return_value = "test_token_12345"

        auth = SiigoAuth(mock_config)
        transport = SyncTransport(mock_config, auth)

        headers = transport._headers()

        assert headers["Partner-Id"] == "test_partner"
        assert headers["Authorization"] == "Bearer test_token_12345"

    @patch.object(SiigoAuth, "token")
    def test_sync_transport_headers_without_partner_id(self, mock_token):
        """Test headers when partner_id is None."""
        mock_token.return_value = "test_token_12345"

        config = Config(
            base_url="https://api.test.siigo.com",
            timeout=30.0,
            username="test_user",
            access_key="test_key",
            partner_id=None,
        )
        auth = SiigoAuth(config)
        transport = SyncTransport(config, auth)

        headers = transport._headers()

        assert headers["Partner-Id"] == ""
        assert headers["Authorization"] == "Bearer test_token_12345"

    @patch.object(SiigoAuth, "token")
    @patch.object(SiigoAuth, "_fetch")
    def test_sync_transport_request_success(self, mock_fetch, mock_token, mock_config):
        """Test successful request."""
        mock_token.return_value = "test_token_12345"

        auth = SiigoAuth(mock_config)
        transport = SyncTransport(mock_config, auth)

        # Mock the client request method
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        transport.client.request = Mock(return_value=mock_response)

        response = transport.request("GET", "https://api.test.siigo.com/v1/test")

        assert response == mock_response
        transport.client.request.assert_called_once()

    @patch.object(SiigoAuth, "token")
    @patch.object(SiigoAuth, "_fetch")
    def test_sync_transport_request_401_retry(self, mock_fetch, mock_token, mock_config):
        """Test that 401 responses trigger token refresh and retry."""
        mock_token.return_value = "test_token_12345"

        auth = SiigoAuth(mock_config)
        transport = SyncTransport(mock_config, auth)

        # Mock the client request method to return 401 first, then 200
        mock_response_401 = Mock()
        mock_response_401.status_code = 401

        mock_response_200 = Mock()
        mock_response_200.status_code = 200
        mock_response_200.json.return_value = {"data": "test"}

        transport.client.request = Mock(side_effect=[mock_response_401, mock_response_200])

        response = transport.request("GET", "https://api.test.siigo.com/v1/test")

        assert response == mock_response_200
        assert transport.client.request.call_count == 2
        mock_fetch.assert_called_once()

    @patch.object(SiigoAuth, "token")
    def test_sync_transport_request_connection_timeout(self, mock_token, mock_config):
        """Test handling of connection timeout errors."""
        mock_token.return_value = "test_token_12345"

        auth = SiigoAuth(mock_config)
        transport = SyncTransport(mock_config, auth)

        # Mock the client to raise ConnectTimeout
        transport.client.request = Mock(side_effect=httpx.ConnectTimeout("Connection timeout"))

        with pytest.raises(APITimeoutError) as exc_info:
            transport.request("GET", "https://api.test.siigo.com/v1/test")

        assert "Connection timeout" in str(exc_info.value)

    @patch.object(SiigoAuth, "token")
    def test_sync_transport_request_http_error(self, mock_token, mock_config):
        """Test handling of HTTP errors."""
        mock_token.return_value = "test_token_12345"

        auth = SiigoAuth(mock_config)
        transport = SyncTransport(mock_config, auth)

        # Mock the client to raise HTTPError
        transport.client.request = Mock(side_effect=httpx.HTTPError("HTTP error"))

        with pytest.raises(APIConnectionError) as exc_info:
            transport.request("GET", "https://api.test.siigo.com/v1/test")

        assert "HTTP error" in str(exc_info.value)

    @patch.object(SiigoAuth, "token")
    def test_sync_transport_request_400_error(self, mock_token, mock_config):
        """Test handling of 400+ status codes."""
        mock_token.return_value = "test_token_12345"

        auth = SiigoAuth(mock_config)
        transport = SyncTransport(mock_config, auth)

        # Mock the client request method
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        transport.client.request = Mock(return_value=mock_response)

        with pytest.raises(APIResponseError) as exc_info:
            transport.request("GET", "https://api.test.siigo.com/v1/test")

        assert exc_info.value.status == 400
        assert exc_info.value.message == "Bad Request"

    @patch.object(SiigoAuth, "token")
    def test_sync_transport_request_with_custom_headers(self, mock_token, mock_config):
        """Test request with custom headers."""
        mock_token.return_value = "test_token_12345"

        auth = SiigoAuth(mock_config)
        transport = SyncTransport(mock_config, auth)

        # Mock the client request method
        mock_response = Mock()
        mock_response.status_code = 200
        transport.client.request = Mock(return_value=mock_response)

        custom_headers = {"X-Custom-Header": "custom_value"}

        transport.request("GET", "https://api.test.siigo.com/v1/test", headers=custom_headers)

        # Check that custom headers were merged with auth headers
        call_args = transport.client.request.call_args
        headers = call_args[1]["headers"]

        assert headers["X-Custom-Header"] == "custom_value"
        assert headers["Authorization"] == "Bearer test_token_12345"
        assert headers["Partner-Id"] == "test_partner"

    @patch.object(SiigoAuth, "token")
    def test_sync_transport_request_with_params(self, mock_token, mock_config):
        """Test request with query parameters."""
        mock_token.return_value = "test_token_12345"

        auth = SiigoAuth(mock_config)
        transport = SyncTransport(mock_config, auth)

        # Mock the client request method
        mock_response = Mock()
        mock_response.status_code = 200
        transport.client.request = Mock(return_value=mock_response)

        params = {"page": 1, "limit": 10}

        transport.request("GET", "https://api.test.siigo.com/v1/test", params=params)

        # Check that params were passed correctly
        call_args = transport.client.request.call_args
        assert call_args[1]["params"] == params
