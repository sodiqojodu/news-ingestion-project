# tests/test_config.py
from config import settings, Settings

def test_settings_defaults():
    # Verify default values are set as expected
    assert settings.ES_HOST == "http://localhost:9200"
    assert settings.UDP_HOST == "0.0.0.0"
    assert settings.UDP_PORT == 9999
    assert settings.SERVICE_PORT == 8000
    assert settings.LOG_LEVEL == "INFO"
