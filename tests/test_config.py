import pytest

from siigo_connector.config import Config


class TestConfig:
    """Test cases for the Config class."""

    def test_config_default_values(self):
        """Test that Config has correct default values."""
        config = Config()

        assert config.base_url == "https://api.siigo.com"
        assert config.timeout == 30.0
        assert config.user_agent == "siigo_connector/0.1.0 (+https://github.com/arendondiosa/siigo-connector-py)"
        assert config.username is None
        assert config.access_key is None
        assert config.partner_id is None

    def test_config_custom_values(self):
        """Test that Config accepts custom values."""
        config = Config(
            base_url="https://custom.api.com",
            timeout=60.0,
            username="test_user",
            access_key="test_key",
            partner_id="test_partner",
        )

        assert config.base_url == "https://custom.api.com"
        assert config.timeout == 60.0
        assert config.username == "test_user"
        assert config.access_key == "test_key"
        assert config.partner_id == "test_partner"

    def test_config_is_frozen(self):
        """Test that Config instances are immutable."""
        config = Config()

        with pytest.raises(Exception):  # dataclass frozen=True raises FrozenInstanceError
            config.base_url = "https://new.api.com"

    def test_config_repr(self):
        """Test Config string representation."""
        config = Config(username="test_user", access_key="test_key", partner_id="test_partner")

        repr_str = repr(config)
        assert "Config" in repr_str
        assert "test_user" in repr_str
        assert "test_key" in repr_str
        assert "test_partner" in repr_str
