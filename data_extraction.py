"""# data_extraction.py
import subprocess

class DataExtractor:
    def _init_(self):
        self.data = {}

    def connect_device(self):
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
        if "device" in result.stdout:
            return True
        else:
            return False

    def extract_data(self):
        try:
            subprocess.run(["adb", "root"], capture_output=True, text=True)
            subprocess.run(["adb", "pull", "/data/data/com.android.providers.telephony/databases/mmssms.db", "./extracted_data/mmssms.db"])
            self.data['sms_database'] = "./extracted_data/mmssms.db"
        except Exception as e:
            print(f"Failed to extract data: {e}")
        return self.data"""

import subprocess
import os

class DataExtractor:
    def __init__(self):
        self.data = {}

    def connect_device(self):
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
        if "device" in result.stdout:
            return True
        else:
            return False

    def extract_data(self):
        try:
            # Ensure the directory exists
            os.makedirs("./extracted_data", exist_ok=True)

            # Root the device (if needed)
            subprocess.run(["adb", "root"], capture_output=True, text=True)

            # Pull the SMS database
            subprocess.run(["adb", "pull", "/data/data/com.android.providers.telephony/databases/mmssms.db", "./extracted_data/mmssms.db"])

            self.data['sms_database'] = "./extracted_data/mmssms.db"
        except Exception as e:
            print(f"Failed to extract data: {e}")
        return self.data


