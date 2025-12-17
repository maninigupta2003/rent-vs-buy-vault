from flask import Flask, request, jsonify
from flask_cors import CORS

from database import init_db, log_event
from vision_extractor import extract_financials
from pii_firewall import scrub_pii
from rent_vs_buy_engine import rent_vs_buy_analysis
from conversation_manager import generate_persuasive_response

app = Flask(__name__)

# 🔥 FORCE CORS (no ambiguity, dev-safe)
CORS(app, resources={r"/*": {"origins": "*"}})

init_db()


@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok"), 200


@app.route("/", methods=["GET"])
def index():
    return jsonify(
        {
            "service": "Rent vs Buy Vault API",
            "status": "running",
        }
    )


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    extracted = extract_financials(file.read())
    log_event("vision_extraction", extracted)
    return jsonify(extracted)


@app.route("/sanitize", methods=["POST"])
def sanitize():
    raw_text = request.json["text"]
    clean = scrub_pii(raw_text)
    log_event("pii_scrub", clean)
    return jsonify({"sanitized": clean})


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    analysis = rent_vs_buy_analysis(
        data["monthly_income"],
        data["annual_rent"],
    )
    return jsonify(analysis)


@app.route("/chat", methods=["POST"])
def chat():
    payload = request.json
    response = generate_persuasive_response(
        payload["analysis"],
        payload.get("convinced", False),
    )
    return jsonify({"message": response})


@app.route("/lead", methods=["POST"])
def capture_lead():
    log_event("lead_capture", request.json)
    return jsonify({"status": "lead_captured"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
