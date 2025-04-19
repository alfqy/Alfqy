from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
DB_FILE = "db.json"

# تحميل البيانات من الملف
def load_data():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

# حفظ البيانات في الملف
def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# التحقق من الجهاز المرسل
@app.route('/check_device', methods=['POST'])
def check_device():
    data = request.json
    code = data.get("device_code")
    db = load_data()
    if code in db:
        return jsonify({"status": "active"})
    else:
        return jsonify({"status": "not_registered"})

# تسجيل الدخول
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    code = data.get("device_code")
    username = data.get("username")
    password = data.get("password")
    
    db = load_data()
    user = db.get(code)
    
    if not user:
        return jsonify({"status": "error", "message": "Device not activated."})

    if user["username"] == username and user["password"] == password:
        expiry = datetime.strptime(user["expires"], "%Y-%m-%d")
        if expiry >= datetime.now():
            return jsonify({"status": "ok", "message": "Login successful."})
        else:
            return jsonify({"status": "expired", "message": "Subscription expired."})
    return jsonify({"status": "error", "message": "Invalid credentials."})

# لتشغيل التطبيق
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
