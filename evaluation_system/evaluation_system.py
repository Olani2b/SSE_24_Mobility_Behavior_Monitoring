from flask import Flask
import logging
from model.json_io import JsonIO
from model.system_configuration import SystemConfiguration
from model.labels_store import LabelsStore
from model.evaluation_report import EvaluationReportGenerator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize Flask application
app = Flask(__name__)

# Paths to configuration and database
CONFIG_PATH = "./data/evaluationSystemConfiguration.json"
DB_PATH = "./data/reports.db"

# Initialize system components
try:
    # Load configuration
    config = SystemConfiguration(CONFIG_PATH)

    # Initialize other components
    label_store = LabelsStore(DB_PATH)
    report_generator = EvaluationReportGenerator()
    json_io = JsonIO(app, config, label_store, report_generator)

    logging.info("[INFO] Evaluation System initialized successfully.")
except Exception as e:
    logging.error(f"[ERROR] Failed to initialize the Evaluation System: {e}")
    raise

# Main entry point
if __name__ == "__main__":
    try:
        # Start the Flask application
        app.run(
            host=config.get("evaluationSystemIP", "127.0.0.1"),
            port=config.get("evaluationSystemPort", 6009)
        )
    except Exception as e:
        logging.error(f"[ERROR] Failed to start the Evaluation System: {e}")
