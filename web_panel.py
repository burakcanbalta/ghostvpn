# web_panel.py

from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/status')
def status():
    try:
        with open("status.json", "r") as f:
            data = json.load(f)
        return jsonify(data)
    except:
        return jsonify({"error": "Status dosyası bulunamadı."})

if __name__ == "__main__":
    app.run(port=5000)