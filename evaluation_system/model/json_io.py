import threading
from flask import request, jsonify
import logging

class JsonIO:
    def __init__(self, app, config, label_store, report_generator):
        self.config = config
        self.label_store = label_store
        self.report_generator = report_generator
        self.setup_routes(app)

    def setup_routes(self, app):
        @app.route("/expertLabels", methods=["POST"])
        def receive_expert_labels():
            data = request.json
            if not data or "uuid" not in data or "label" not in data:
                return jsonify({"error": "Invalid label format"}), 400

            self.label_store.store_expert_label(data["uuid"], data["label"])
            logging.info(f"Expert label received: {data}")
            self._check_and_trigger_evaluation()
            return jsonify({"status": "Expert label stored"}), 200

        @app.route("/classifierLabels", methods=["POST"])
        def receive_classifier_labels():
            data = request.json
            if not data or "uuid" not in data or "label" not in data:
                return jsonify({"error": "Invalid label format"}), 400

            self.label_store.store_classifier_label(data["uuid"], data["label"])
            logging.info(f"Classifier label received: {data}")
            self._check_and_trigger_evaluation()
            return jsonify({"status": "Classifier label stored"}), 200

    def _check_and_trigger_evaluation(self):
        """
        Checks if the number of labels meets the threshold and triggers evaluation in a new thread.
        """
        labels = self.label_store.get_matching_labels()
        if len(labels) >= self.config.get("labelsThreshold", 10):
            logging.info("Threshold met. Triggering evaluation.")
            evaluation_thread = threading.Thread(target=self._evaluate, args=(labels,))
            evaluation_thread.start()

    def _evaluate(self, labels):
        """
        Evaluates labels, generates a report, and handles user decision.
        """
        try:
            # Generate the report
            report = self.report_generator.generate_evaluation_report(labels)

            # Clear labels from the database
            self.label_store.clear_labels()

            # Save the report
            self.report_generator.save_to_json(report, "./data/evaluationReport.json")
            logging.info(f"Evaluation report generated: {report}")

            # Display the report to the user
            print("Evaluation Report:", report)

            # Prompt user for decision
            user_input = input("Did the test pass? (yes/no): ").strip().lower()
            if user_input == "no":
                self._send_retrain_message()
        except Exception as e:
            logging.error(f"Error during evaluation: {e}")

    def _send_retrain_message(self):
        """
        Sends a 'retrain' message to the messaging system.
        """
        import requests
        try:
            url = f"http://{self.config.get('messagingSystemIP')}:{self.config.get('messagingSystemPort')}/api"
            message = {"action": "retrain", "reason": "Test failed"}
            response = requests.post(url, json=message, timeout=5)
            if response.status_code == 200:
                logging.info("Retrain message sent successfully.")
            else:
                logging.error(f"Failed to send retrain message. Status code: {response.status_code}")
        except requests.exceptions.Timeout:
            logging.error("Request to messaging system timed out.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending retrain message: {e}")
