from flask import Flask, request

app = Flask(__name__)

last_alert = None

@app.route("/alert", methods=["POST"])
def alert():
    global last_alert
    last_alert = request.json
    print("Nouvelle alerte reçue :", last_alert)
    return {"status": "received"}

@app.route("/alert/next", methods=["GET"])
def get_alert():
    global last_alert
    if last_alert:
        data = last_alert
        last_alert = None
        return {"alert": data}
    return {"alert": None}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
