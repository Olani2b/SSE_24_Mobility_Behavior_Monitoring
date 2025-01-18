import json
import logging

class SystemConfiguration:
    def __init__(self, config_path):
        """
        Loads system configuration from the specified JSON file.
        """
        self.config_path = config_path
        self.config = {}
        self.load_config()

    def load_config(self):
        """
        Loads configuration from the JSON file.
        """
        try:
            with open(self.config_path, "r") as f:
                self.config = json.load(f)
                logging.info(f"[INFO] Configuration loaded from {self.config_path}")
        except FileNotFoundError:
            logging.error(f"[ERROR] Configuration file not found: {self.config_path}")
        except json.JSONDecodeError as e:
            logging.error(f"[ERROR] Failed to parse configuration file: {e}")

    def get(self, key, default=None):
        """
        Retrieves a configuration value.

        :param key: Key to look up.
        :param default: Default value if the key is not found.
        :return: Configuration value or default.
        """
        return self.config.get(key, default)
