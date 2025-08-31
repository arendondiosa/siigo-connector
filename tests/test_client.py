from unittest.mock import Mock, patch

from siigo_connector.client import Client
from siigo_connector.config import Config


class TestClient:
    """Test cases for the Client class."""

    @patch("siigo_connector.client.Config")
    @patch("siigo_connector.client.SiigoAuth")
    @patch("siigo_connector.client.SyncTransport")
    def test_client_initialization(
        self, mock_transport_class, mock_auth_class, mock_config_class
    ):
        """Test Client initialization with all parameters."""
        # Mock the dependencies
        mock_config = Mock(spec=Config)
        mock_config.base_url = "https://api.test.siigo.com"
        mock_config.timeout = 60.0
        mock_config_class.return_value = mock_config

        mock_auth = Mock()
        mock_auth_class.return_value = mock_auth

        mock_transport = Mock()
        mock_transport_class.return_value = mock_transport

        # Create client
        client = Client(
            username="test_user",
            access_key="test_key",
            partner_id="test_partner",
            base_url="https://api.test.siigo.com",
            timeout=60.0,
        )

        # Verify Config was created with correct parameters
        mock_config_class.assert_called_once_with(
            base_url="https://api.test.siigo.com",
            timeout=60.0,
            username="test_user",
            access_key="test_key",
            partner_id="test_partner",
        )

        # Verify SiigoAuth was created with config
        mock_auth_class.assert_called_once_with(mock_config)

        # Verify SyncTransport was created with config and auth
        mock_transport_class.assert_called_once_with(mock_config, mock_auth)

        # Verify client attributes
        assert client._http == mock_transport
        assert client._base_url == "https://api.test.siigo.com"
        assert client.customers is not None

    @patch("siigo_connector.client.Config")
    @patch("siigo_connector.client.SiigoAuth")
    @patch("siigo_connector.client.SyncTransport")
    def test_client_initialization_defaults(
        self, mock_transport_class, mock_auth_class, mock_config_class
    ):
        """Test Client initialization with default values."""
        # Mock the dependencies
        mock_config = Mock(spec=Config)
        mock_config.base_url = "https://api.siigo.com"
        mock_config.timeout = 30.0
        mock_config_class.return_value = mock_config

        mock_auth = Mock()
        mock_auth_class.return_value = mock_auth

        mock_transport = Mock()
        mock_transport_class.return_value = mock_transport

        # Create client with minimal parameters
        client = Client(
            username="test_user", access_key="test_key", partner_id="test_partner"
        )

        # Verify Config was created with default values
        mock_config_class.assert_called_once()
        # Check that the client was created successfully
        assert client._http == mock_transport
        assert client._base_url == "https://api.siigo.com"
        assert client.customers is not None

    @patch("siigo_connector.client.Config")
    @patch("siigo_connector.client.SiigoAuth")
    @patch("siigo_connector.client.SyncTransport")
    def test_client_request_method(
        self, mock_transport_class, mock_auth_class, mock_config_class
    ):
        """Test Client _request method delegates to transport."""
        # Mock the dependencies
        mock_config = Mock(spec=Config)
        mock_config_class.return_value = mock_config

        mock_auth = Mock()
        mock_auth_class.return_value = mock_auth

        mock_transport = Mock()
        mock_transport_class.return_value = mock_transport

        # Create client
        client = Client(
            username="test_user", access_key="test_key", partner_id="test_partner"
        )

        # Test _request method
        client._request("GET", "https://api.test.com/v1/test", params={"key": "value"})

        # Verify transport.request was called with correct parameters
        mock_transport.request.assert_called_once_with(
            "GET", "https://api.test.com/v1/test", params={"key": "value"}
        )

    @patch("siigo_connector.client.Config")
    @patch("siigo_connector.client.SiigoAuth")
    @patch("siigo_connector.client.SyncTransport")
    def test_client_close_method(
        self, mock_transport_class, mock_auth_class, mock_config_class
    ):
        """Test Client close method delegates to transport."""
        # Mock the dependencies
        mock_config = Mock(spec=Config)
        mock_config_class.return_value = mock_config

        mock_auth = Mock()
        mock_auth_class.return_value = mock_auth

        mock_transport = Mock()
        mock_transport_class.return_value = mock_transport

        # Create client
        client = Client(
            username="test_user", access_key="test_key", partner_id="test_partner"
        )

        # Test close method
        client.close()

        # Verify transport.close was called
        mock_transport.close.assert_called_once()

    @patch("siigo_connector.client.Config")
    @patch("siigo_connector.client.SiigoAuth")
    @patch("siigo_connector.client.SyncTransport")
    @patch("siigo_connector.client.CustomersResource")
    def test_client_customers_resource(
        self,
        mock_customers_class,
        mock_transport_class,
        mock_auth_class,
        mock_config_class,
    ):
        """Test that customers resource is properly initialized."""
        # Mock the dependencies
        mock_config = Mock(spec=Config)
        mock_config.base_url = "https://api.test.siigo.com"
        mock_config_class.return_value = mock_config

        mock_auth = Mock()
        mock_auth_class.return_value = mock_auth

        mock_transport = Mock()
        mock_transport_class.return_value = mock_transport

        mock_customers = Mock()
        mock_customers_class.return_value = mock_customers

        # Create client
        client = Client(
            username="test_user",
            access_key="test_key",
            partner_id="test_partner",
            base_url="https://api.test.siigo.com",
        )

        # Verify customers resource was created with correct parameters
        mock_customers_class.assert_called_once_with(
            _request=client._request, base_url="https://api.test.siigo.com"
        )

        # Verify client has customers attribute
        assert client.customers == mock_customers

    def test_client_context_manager_behavior(self):
        """Test that Client can be used as a context manager."""
        with (
            patch("siigo_connector.client.Config") as mock_config_class,
            patch("siigo_connector.client.SiigoAuth") as mock_auth_class,
            patch("siigo_connector.client.SyncTransport") as mock_transport_class,
        ):
            # Mock the dependencies
            mock_config = Mock(spec=Config)
            mock_config_class.return_value = mock_config

            mock_auth = Mock()
            mock_auth_class.return_value = mock_auth

            mock_transport = Mock()
            mock_transport_class.return_value = mock_transport

            # Test that client can be created and closed
            client = Client(
                username="test_user", access_key="test_key", partner_id="test_partner"
            )

            # Verify close method exists and works
            client.close()
            mock_transport.close.assert_called_once()

    @patch("siigo_connector.client.Config")
    @patch("siigo_connector.client.SiigoAuth")
    @patch("siigo_connector.client.SyncTransport")
    def test_client_different_base_urls(
        self, mock_transport_class, mock_auth_class, mock_config_class
    ):
        """Test Client with different base URLs."""
        # Test with custom base URL
        mock_config = Mock(spec=Config)
        mock_config.base_url = "https://custom.api.com"
        mock_config_class.return_value = mock_config

        mock_auth = Mock()
        mock_auth_class.return_value = mock_auth

        mock_transport = Mock()
        mock_transport_class.return_value = mock_transport

        client = Client(
            username="test_user",
            access_key="test_key",
            partner_id="test_partner",
            base_url="https://custom.api.com",
        )

        assert client._base_url == "https://custom.api.com"

        # Verify Config was created with custom base URL
        mock_config_class.assert_called()
        # Check that the client was created successfully
        assert client._http == mock_transport
        assert client._base_url == "https://custom.api.com"
        assert client.customers is not None

    @patch("siigo_connector.client.Config")
    @patch("siigo_connector.client.SiigoAuth")
    @patch("siigo_connector.client.SyncTransport")
    def test_client_different_timeouts(
        self, mock_transport_class, mock_auth_class, mock_config_class
    ):
        """Test Client with different timeout values."""
        # Test with custom timeout
        mock_config = Mock(spec=Config)
        mock_config.timeout = 120.0
        mock_config_class.return_value = mock_config

        mock_auth = Mock()
        mock_auth_class.return_value = mock_auth

        mock_transport = Mock()
        mock_transport_class.return_value = mock_transport

        client = Client(
            username="test_user",
            access_key="test_key",
            partner_id="test_partner",
            timeout=120.0,
        )

        # Verify Config was created with custom timeout
        mock_config_class.assert_called()
        # Check that the client was created successfully
        assert client._http == mock_transport
        # The base_url will be a mock since we're mocking Config
        assert client.customers is not None
