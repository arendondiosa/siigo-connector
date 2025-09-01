from siigo_connector.errors import (
    APIConnectionError,
    APIResponseError,
    APITimeoutError,
    YourAPIError,
)


class TestErrors:
    """Test cases for error classes."""

    def test_your_api_error_inheritance(self):
        """Test that all errors inherit from YourAPIError."""
        assert issubclass(APIConnectionError, YourAPIError)
        assert issubclass(APITimeoutError, YourAPIError)
        assert issubclass(APIResponseError, YourAPIError)

    def test_api_response_error_creation(self):
        """Test APIResponseError creation and attributes."""
        error = APIResponseError(404, "Not Found")

        assert error.status == 404
        assert error.message == "Not Found"
        assert str(error) == "404: Not Found"

    def test_api_response_error_different_status_codes(self):
        """Test APIResponseError with different status codes."""
        error_400 = APIResponseError(400, "Bad Request")
        error_500 = APIResponseError(500, "Internal Server Error")

        assert error_400.status == 400
        assert error_500.status == 500
        assert str(error_400) == "400: Bad Request"
        assert str(error_500) == "500: Internal Server Error"

    def test_api_response_error_empty_message(self):
        """Test APIResponseError with empty message."""
        error = APIResponseError(204, "")

        assert error.status == 204
        assert error.message == ""
        assert str(error) == "204: "

    def test_api_connection_error_creation(self):
        """Test APIConnectionError creation."""
        error = APIConnectionError("Connection failed")

        assert str(error) == "Connection failed"
        assert isinstance(error, YourAPIError)

    def test_api_timeout_error_creation(self):
        """Test APITimeoutError creation."""
        error = APITimeoutError("Request timed out")

        assert str(error) == "Request timed out"
        assert isinstance(error, YourAPIError)
