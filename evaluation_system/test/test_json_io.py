import pytest
from flask import Flask
from model.json_io import JsonIO
from model.evaluation_report import EvaluationReportGenerator
from model.system_configuration import SystemConfiguration
from model.labels_store import LabelsStore
import tempfile
import json
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

@pytest.fixture
def labels_store():
    with tempfile.NamedTemporaryFile(suffix=".db") as temp_db:
        db_path = temp_db.name
        store = LabelsStore(db_path)
        store._setup_database()
        yield store

@pytest.fixture
def json_io(temp_config_file, labels_store):
    local_app = Flask(__name__)
    report_generator = EvaluationReportGenerator()
    config = SystemConfiguration(temp_config_file)
    json_io_instance = JsonIO(local_app, config, labels_store, report_generator)
    return {
        "app": local_app,
        "json_io": json_io_instance
    }
    #return JsonIO(local_app, config, labels_store, report_generator)

def test_receive_expert_labels(json_io):
    #app = json_io._app
    app = json_io["app"]
    with app.test_client() as client:
        response = client.post("/expertLabels", json={"uuid": "wrwewr-ewrewr-werwrew-werrwe", "label": "Regular"})
        assert response.status_code == 200

def test_receive_classifier_labels(json_io):
    #app = json_io._app
    app = json_io["app"]
    with app.test_client() as client:
        response = client.post("/classifierLabels", json={"uuid": "wrwewr-ewrewr-werwrew-werrwe", "label": "Regular"})
        assert response.status_code == 200
