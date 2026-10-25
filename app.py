from datetime import datetime, timezone
from flask import Flask, jsonify, render_template, request
from collections import Counter

app = Flask(__name__)

events = []


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "connect-src 'self'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'none'"
    )
    return response


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/simulate")
def simulate():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        app.logger.warning("Rejected invalid JSON request")
        return jsonify({"error": "A JSON object is required"}), 400

    scenario = data.get("scenario")

    if scenario not in {"normal", "suspicious"}:
        app.logger.warning("Rejected invalid test scenario")
        return jsonify({"error": "Invalid test scenario"}), 400

    if scenario == "normal":
        decision = "ALLOW"
        reason = "Normal simulated advertisement"
        app.logger.info("AdShield allowed a normal test event")
    else:
        decision = "BLOCK"
        reason = "Suspicious behavior detected by simulation rule"
        app.logger.warning("AdShield blocked a suspicious test event")

    event = {
        "scenario": scenario,
        "decision": decision,
        "reason": reason,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    events.append(event)

    return jsonify(event), 200


@app.get("/dashboard")
def dashboard():
    counts = Counter(event["decision"] for event in events)

    return jsonify({
        "total_events": len(events),
        "allowed": counts["ALLOW"],
        "blocked": counts["BLOCK"],
        "recent_events": list(reversed(events[-10:]))
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
