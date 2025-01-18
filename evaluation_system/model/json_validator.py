from jsonschema import validate, ValidationError
import json
import logging

class JsonValidator:
    def __init__(self):
        """
        Initializes the JSON Validator.
        """
        logging.info("[INFO] JSON Validator initialized.")

    def validate(self, data, schema_path):
        """
        Validates the provided data against the schema.

        :param data: The JSON data to validate.
        :param schema_path: Path to the schema file.
        :raises ValidationError: If the validation fails.
        """
        try:
            with open(schema_path, "r") as f:
                schema = json.load(f)
            validate(instance=data, schema=schema)
            logging.info("[INFO] JSON validation successful.")
        except FileNotFoundError:
            logging.error(f"[ERROR] Schema file not found: {schema_path}")
            raise
        except ValidationError as e:
            logging.error(f"[ERROR] JSON validation failed: {e}")
            raise
        except Exception as e:
            logging.error(f"[ERROR] Unexpected error during JSON validation: {e}")
            raise
