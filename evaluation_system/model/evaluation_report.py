import json

class EvaluationReportGenerator:
    def generate_evaluation_report(self, labels):
        total_errors = sum(1 for label in labels if label["expert_label"] != label["classifier_label"])
        max_consecutive_errors = self._calculate_max_consecutive_errors(labels)
        return {
            "totalErrors": total_errors,
            "maxConsecutiveErrors": max_consecutive_errors
        }

    def _calculate_max_consecutive_errors(self, labels):
        max_streak = 0
        current_streak = 0
        for label in labels:
            if label["expert_label"] != label["classifier_label"]:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
        return max_streak

    def save_to_json(self, report, file_path):
        with open(file_path, "w") as f:
            json.dump(report, f, indent=4)
