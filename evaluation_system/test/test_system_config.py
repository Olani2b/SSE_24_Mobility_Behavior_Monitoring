import pytest
import json
import tempfile
from model.system_configuration import SystemConfiguration
import os
@pytest.fixture
def temp_config_file():
    content = {
        "labelsThreshold": 10,
        "evaluationSystemIP": "127.0.0.1",
        "evaluationSystemPort": 6009
    }
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        json.dump(content, temp_file)
        temp_file.flush()
        yield temp_file.name
    os.remove(temp_file.name)

def test_system_configuration(temp_config_file):
    config = SystemConfiguration(temp_config_file)
    assert config.get("labelsThreshold") == 10
    assert config.get("evaluationSystemIP") == "127.0.0.1"
    assert config.get("evaluationSystemPort") == 6009
