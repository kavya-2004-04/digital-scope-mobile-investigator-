from flask import Flask, jsonify, render_template, request
import subprocess
import os

class DataExtractor:
    def __init__(self):
        self.data = {}

    def connect_device(self):
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
        return "device" in result.stdout.splitlines()[1]

    def extract_data(self):
        try:
            subprocess.run(["adb", "root"], capture_output=True, text=True)
            os.makedirs("./extracted_data", exist_ok=True)
            subprocess.run(["adb", "pull", "/data/data/com.android.providers.telephony/databases/mmssms.db", "./extracted_data/mmssms.db"])
            self.data['sms_database'] = "./extracted_data/mmssms.db"
        except Exception as e:
            print(f"Failed to extract data: {e}")
        return self.data

app = Flask(__name__)
extractor = DataExtractor()

def run_adb_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/adb_devices', methods=['GET'])
def adb_devices():
    output = run_adb_command(["adb", "devices"])
    return jsonify({"output": output})

@app.route('/device_info', methods=['GET'])
def device_info():
    device_id = request.args.get('device_id')
    output = run_adb_command(["adb", "-s", device_id, "shell", "getprop", "ro.product.model"])
    return jsonify({"device_info": output})

@app.route('/battery_status', methods=['GET'])
def battery_status():
    device_id = request.args.get('device_id')
    output = run_adb_command(["adb", "-s", device_id, "shell", "dumpsys", "battery"])
    return jsonify({"battery_status": output})

@app.route('/screenshot', methods=['GET'])
def screenshot():
    device_id = request.args.get('device_id')
    screenshot_path = "/sdcard/screenshot.png"
    output = run_adb_command(["adb", "-s", device_id, "shell", "screencap", "-p", screenshot_path])
    if "Error" not in output:
        run_adb_command(["adb", "-s", device_id, "pull", screenshot_path, "./screenshot.png"])
        return jsonify({"screenshot": "Screenshot saved as screenshot.png"})
    else:
        return jsonify({"error": output})

@app.route('/installed_packages', methods=['GET'])
def installed_packages():
    device_id = request.args.get('device_id')
    output = run_adb_command(["adb", "-s", device_id, "shell", "pm", "list", "packages"])
    return jsonify({"installed_packages": output})

@app.route('/reboot_device', methods=['POST'])
def reboot_device():
    device_id = request.form.get('device_id')
    output = run_adb_command(["adb", "-s", device_id, "reboot"])
    return jsonify({"reboot_status": output})

@app.route('/logcat', methods=['GET'])
def logcat():
    device_id = request.args.get('device_id')
    output = run_adb_command(["adb", "-s", device_id, "logcat", "-d"])
    return jsonify({"logcat": output})

# @app.route('/push_file', methods=['POST'])
# def push_file():
#     device_id = request.form.get('device_id')
#     local_path = request.form.get('file_path')
#     remote_path = "/sdcard/remote_file"
#     output = run_adb_command(["adb", "-s", device_id, "push", local_path, remote_path])
#     return jsonify({"push_status": output})

# @app.route('/pull_file', methods=['GET'])
# def pull_file():
#     device_id = request.args.get('device_id')
#     remote_path = request.args.get('file_path')
#     local_path = "./local_file"
#     output = run_adb_command(["adb", "-s", device_id, "pull", remote_path, local_path])
#     return jsonify({"pull_status": output})

@app.route('/uninstall_app', methods=['POST'])
def uninstall_app():
    device_id = request.form.get('device_id')
    package_name = request.form.get('package_name')
    method = request.form.get('_method')
    if method == 'DELETE':
        output = run_adb_command(["adb", "-s", device_id, "uninstall", package_name])
        return jsonify({"uninstall_status": output})
    return jsonify({"error": "Invalid method"}), 405

# @app.route('/install_app', methods=['POST'])
# def install_app():
#     device_id = request.form.get('device_id')
#     apk_path = request.form.get('apk_path')
#     output = run_adb_command(["adb", "-s", device_id, "install", apk_path])
#     return jsonify({"install_status": output})

@app.route('/extract_data', methods=['GET'])
def extract_data():
    if extractor.connect_device():
        extracted_data = extractor.extract_data()
        if 'sms_database' in extracted_data:
            return jsonify({"status": "success", "data": extracted_data})
        else:
            return jsonify({"status": "failed", "message": "Data extraction failed."})
    else:
        return jsonify({"status": "failed", "message": "No device connected."})

if __name__ == '__main__':
    app.run(debug=True)
