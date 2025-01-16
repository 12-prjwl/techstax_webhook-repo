import hmac
import hashlib
from flask import Blueprint, request, jsonify, current_app, Response, json
from datetime import datetime

main = Blueprint("main", __name__)

# GitHub secret passcode
GITHUB_SECRET = "job123"


def format_timestamp():
    now = datetime.utcnow()
    day = now.day
    suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return now.strftime(f"%d{suffix} %B %Y - %I:%M %p UTC")

# Webhook endpoint
@main.route("/webhook", methods=["POST"])
def webhook():
    # Verify GitHub signature
    signature = request.headers.get("X-Hub-Signature-256")
    if not is_valid_signature(request.data, signature):
        return jsonify({"error": "Invalid signature"}), 401

    data = request.json

    # Parse event type
    event = request.headers.get("X-GitHub-Event")
    if event == "push":
        payload = {
            "action": "Push",
            "author": data["pusher"]["name"],
            "from_branch": "",
            "to_branch": data["ref"].split("/")[-1], 
            "timestamp": format_timestamp()
        }
    elif event == "pull_request":
        action = data["action"]
        if action in ["opened", "reopened"]:
            payload = {
                "action": "Pull Request",
                "author": data["pull_request"]["user"]["login"],
                "from_branch": data["pull_request"]["head"]["ref"],
                "to_branch": data["pull_request"]["base"]["ref"],
                "timestamp": format_timestamp()
            }
        elif action == "closed" and data["pull_request"]["merged"]:
            payload = {
                "action": "Merge",
                "author": data["pull_request"]["user"]["login"],
                "from_branch": data["pull_request"]["head"]["ref"],
                "to_branch": data["pull_request"]["base"]["ref"],
                "timestamp": format_timestamp()
            }
        else:
            return jsonify({"message": "Event ignored"}), 200
    else:
        return jsonify({"message": "Event ignored"}), 200

    # Storing the payload in MongoDB
    try:
        db = current_app.mongo
        db.events.insert_one(payload)
        return jsonify({"message": "Event stored successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def is_valid_signature(payload, signature):
    if not signature:
        return False
    secret = bytes(GITHUB_SECRET, "utf-8")
    hash = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    expected_signature = f"sha256={hash}"
    return hmac.compare_digest(expected_signature, signature)

from flask import jsonify

@main.route("/events", methods=["GET"])
def get_events():
    db = current_app.mongo
    events = list(db.events.find({}, {"_id": 0}))  # Exclude `_id` field from response
    return jsonify(events)

