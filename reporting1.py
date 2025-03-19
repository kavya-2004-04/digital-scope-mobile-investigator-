# reporting.py
class ReportGenerator:
    def _init_(self, analysis_results):
        self.analysis_results = analysis_results

    def generate_report(self):
        report = "Analysis Report:\n"
        report += f"Total SMS Messages: {self.analysis_results.get('total_sms', 'N/A')}\n"
        return report

    def save_report(self, filename="report.txt"):
        with open(filename, "w") as file:
            file.write(self.generate_report())
