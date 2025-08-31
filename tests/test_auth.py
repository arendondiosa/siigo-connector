import pytest
import time
from unittest.mock import Mock, patch

from siigo_connector.auth import SiigoAuth
from siigo_connector.config import Config
from siigo_connector.errors import APIResponseError


class TestSiigoAuth:
    """Test cases for the SiigoAuth class."""

    def test_siigo_auth_initialization(self, mock_config):
        """Test SiigoAuth initialization."""
        auth = SiigoAuth(mock_config)

        assert auth._cfg == mock_config
        assert auth._token is None
        assert auth._exp_ts is None

    def test_siigo_auth_missing_credentials(self, mock_config):
        """Test that SiigoAuth raises error when credentials are missing."""
        config = Config(
            base_url="https://api.test.siigo.com",
            timeout=30.0,
            username=None,
            access_key=None,
            partner_id=None,
        )
        auth = SiigoAuth(config)

        with pytest.raises(
            ValueError, match="username, access_key and partner_id are required"
        ):
            auth.token()

    @patch("httpx.Client")
    def test_siigo_auth_successful_fetch(
        self, mock_client_class, mock_config, mock_auth_response
    ):
        """Test successful token fetch."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_auth_response
        mock_client.post.return_value = mock_response
        mock_client_class.return_value.__enter__.return_value = mock_client

        auth = SiigoAuth(mock_config)
        token = auth.token()

        assert token == "test_token_12345"
        assert auth._token == "test_token_12345"
        assert auth._exp_ts is not None
        assert auth._exp_ts > time.time()

    @patch("httpx.Client")
    def test_siigo_auth_without_expires_in(self, mock_client_class, mock_config):
        """Test token fetch when Siigo doesn't return expires_in."""
        mock_auth_response = {
            "access_token": "test_token_12345",
            "token_type": "Bearer",
        }

        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_auth_response
        mock_client.post.return_value = mock_response
        mock_client_class.return_value.__enter__.return_value = mock_client

        auth = SiigoAuth(mock_config)
        token = auth.token()

        assert token == "test_token_12345"
        assert auth._token == "test_token_12345"
        assert auth._exp_ts is None

    @patch("httpx.Client")
    def test_siigo_auth_http_error(self, mock_client_class, mock_config):
        """Test handling of HTTP errors during token fetch."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_client.post.return_value = mock_response
        mock_client_class.return_value.__enter__.return_value = mock_client

        auth = SiigoAuth(mock_config)

        with pytest.raises(APIResponseError) as exc_info:
            auth.token()

        assert exc_info.value.status == 401
        assert exc_info.value.message == "Unauthorized"

    @patch("httpx.Client")
    def test_siigo_auth_no_token_in_response(self, mock_client_class, mock_config):
        """Test handling when no access_token is in response."""
        mock_auth_response = {
            "token_type": "Bearer"
            # Missing access_token
        }

        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_auth_response
        mock_client.post.return_value = mock_response
        mock_client_class.return_value.__enter__.return_value = mock_client

        auth = SiigoAuth(mock_config)

        with pytest.raises(APIResponseError) as exc_info:
            auth.token()

        assert exc_info.value.status == 500
        assert "No access_token" in exc_info.value.message

    @patch("httpx.Client")
    def test_siigo_auth_token_caching(
        self, mock_client_class, mock_config, mock_auth_response
    ):
        """Test that tokens are cached and reused."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_auth_response
        mock_client.post.return_value = mock_response
        mock_client_class.return_value.__enter__.return_value = mock_client

        auth = SiigoAuth(mock_config)

        # First call should fetch token
        token1 = auth.token()
        assert token1 == "test_token_12345"

        # Second call should use cached token
        token2 = auth.token()
        assert token2 == "test_token_12345"

        # Should only call the API once
        mock_client.post.assert_called_once()

    @patch("httpx.Client")
    def test_siigo_auth_token_expiration(self, mock_client_class, mock_config):
        """Test that expired tokens trigger a new fetch."""
        # First response with short expiration
        mock_auth_response1 = {
            "access_token": "old_token",
            "expires_in": 1,  # 1 second expiration
        }

        # Second response
        mock_auth_response2 = {"access_token": "new_token", "expires_in": 3600}

        mock_client = Mock()
        mock_response1 = Mock()
        mock_response1.status_code = 200
        mock_response1.json.return_value = mock_auth_response1

        mock_response2 = Mock()
        mock_response2.status_code = 200
        mock_response2.json.return_value = mock_auth_response2

        mock_client.post.side_effect = [mock_response1, mock_response2]
        mock_client_class.return_value.__enter__.return_value = mock_client

        auth = SiigoAuth(mock_config)

        # First call
        token1 = auth.token()
        assert token1 == "old_token"

        # Wait for token to expire
        time.sleep(1.1)

        # Second call should fetch new token
        token2 = auth.token()
        assert token2 == "new_token"

        # Should have called the API twice
        assert mock_client.post.call_count == 2
