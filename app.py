from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# Dernière alerte reçue depuis RoboFlow
last_alert = None


@app.route("/")
def index():
    # Page du dashboard
    return render_template("dashboard.html")


@app.route("/alert", methods=["POST"])
def alert():
    """
    Endpoint appelé par ton script test_robotflow.py
    """
    global last_alert
    data = request.get_json() or {}

    # On normalise les champs
    helmet = bool(data.get("helmet"))
    no_helmet = bool(data.get("no_helmet"))

    last_alert = {
        "helmet": helmet,
        "no_helmet": no_helmet,
        "received_at": datetime.utcnow().isoformat() + "Z"
    }

    print("🔥 Nouvelle alerte reçue :", last_alert)
    return jsonify({"status": "received"})


@app.route("/alert/next", methods=["GET"])
def get_alert():
    """
    Endpoint consulté par le dashboard (JS) toutes les X secondes
    """
    if last_alert is None:
        return jsonify({"alert": None})
    return jsonify({"alert": last_alert})


if __name__ == "__main__":
    # Local uniquement (sur Render, c'est gunicorn qui lance)
    app.run(host="0.0.0.0", port=5000, debug=True)
