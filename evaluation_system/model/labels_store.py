import sqlite3

class LabelsStore:
    def __init__(self, db_path):
        self.db_path = db_path
        self._setup_database()

    def _setup_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expert_labels (
                uuid TEXT PRIMARY KEY,
                label TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS classifier_labels (
                uuid TEXT PRIMARY KEY,
                label TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def store_expert_label(self, uuid, label):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO expert_labels (uuid, label) VALUES (?, ?)", (uuid, label))
        conn.commit()
        conn.close()

    def store_classifier_label(self, uuid, label):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO classifier_labels (uuid, label) VALUES (?, ?)", (uuid, label))
        conn.commit()
        conn.close()

    def get_matching_labels(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.uuid, e.label AS expert_label, c.label AS classifier_label
            FROM expert_labels e
            JOIN classifier_labels c ON e.uuid = c.uuid
        """)
        labels = cursor.fetchall()
        conn.close()
        return [{"uuid": row[0], "expert_label": row[1], "classifier_label": row[2]} for row in labels]

    def clear_labels(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expert_labels")
        cursor.execute("DELETE FROM classifier_labels")
        conn.commit()
        conn.close()
