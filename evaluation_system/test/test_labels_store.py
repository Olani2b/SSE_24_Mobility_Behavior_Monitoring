import pytest
import tempfile
from model.labels_store import LabelsStore

@pytest.fixture
def labels_store():
    with tempfile.NamedTemporaryFile(suffix=".db") as temp_db:
        db_path = temp_db.name
        store = LabelsStore(db_path)
        store._setup_database()
        yield store

def test_store_and_retrieve_labels(labels_store):
    labels_store.store_expert_label("uuid1", "Regular")
    labels_store.store_classifier_label("uuid1", "Anomalous")
    labels = labels_store.get_matching_labels()
    assert len(labels) == 1
    assert labels[0]["expert_label"] == "Regular"
    assert labels[0]["classifier_label"] == "Anomalous"

def test_clear_labels(labels_store):
    labels_store.store_expert_label("uuid1", "Regular")
    labels_store.store_classifier_label("uuid1", "Anomalous")
    labels_store.clear_labels()
    labels = labels_store.get_matching_labels()
    assert len(labels) == 0
