import pytest
from model.json_validator import JsonValidator
from jsonschema import ValidationError
import tempfile
import json
import os

def test_json_validation_success():
    schema = {
        "type": "object",
        "properties": {
            "uuid": {"type": "string"},
            "label": {"type": "string"}
        },
        "required": ["uuid", "label"]
    }
    data = {"uuid": "wrwewr-ewrewr-werwrew-werrwe", "label": "Regular"}
    json_validator = JsonValidator()
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        json.dump(schema, temp_file)
        temp_file.flush()
        assert json_validator.validate(data, temp_file.name) is None
    os.remove(temp_file.name)

def test_json_validation_failure():
    schema = {
        "type": "object",
        "properties": {
            "uuid": {"type": "string"},
            "label": {"type": "string"}
        },
        "required": ["uuid", "label"]
    }
    data = {"uuid": "wrwewr-ewrewr-werwrew-werrwe"}
    json_validator = JsonValidator()
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        json.dump(schema, temp_file)
        temp_file.flush()
        with pytest.raises(ValidationError):
            json_validator.validate(data, temp_file.name)
    os.remove(temp_file.name)
