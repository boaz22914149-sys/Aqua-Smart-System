from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# ఆటో మోడ్ మరియు లాస్ట్ అప్‌డేట్ టైమ్ యాడ్ చేశాం
live_data = {
    "ph": 7.4,
    "do": 6.8,
    "turbidity": 2.3,
    "temp": 27.5,
    "sound_level": "Normal",
    "feeder_active": False,
    "aerator_active": False,
    "auto_mode": True,
    "last_update": "Waiting for device..."
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/update', methods=['POST'])
def update_data():
    global live_data
    content = request.get_json()
    if content:
        live_data["ph"] = content.get("ph", live_data["ph"])
        live_data["do"] = content.get("do", live_data["do"])
        live_data["turbidity"] = content.get("turbidity", live_data["turbidity"])
        live_data["temp"] = content.get("temp", live_data["temp"])
        live_data["sound_level"] = content.get("sound_level", live_data["sound_level"])
        
        # డేటా వచ్చిన టైమ్ రికార్డ్ అవుతుంది
        now = datetime.now()
        live_data["last_update"] = now.strftime("%H:%M:%S")

        return jsonify({
            "status": "success",
            "feeder": live_data["feeder_active"],
            "aerator": live_data["aerator_active"],
            "auto_mode": live_data["auto_mode"]
        }), 200
    return jsonify({"status": "no data"}), 400

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(live_data)

@app.route('/api/control', methods=['POST'])
def control_device():
    global live_data
    content = request.get_json()
    action = content.get("action")
    state = content.get("state")

    if action == "feeder":
        live_data["feeder_active"] = state
    elif action == "aerator":
        live_data["aerator_active"] = state
    elif action == "auto_mode":
        live_data["auto_mode"] = state

    return jsonify({"status": "updated", "action": action, "state": state})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)