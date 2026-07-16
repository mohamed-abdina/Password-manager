"""
app.py

Flask web server that provides a browser-based UI for the password manager.
Reuses load_data / save_data / generate_password / check_strength from password_manager.py.
"""

from flask import Flask, jsonify, render_template, request
from password_manager import (
    check_strength,
    generate_password,
    load_data,
    save_data,
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/passwords", methods=["GET"])
def list_passwords():
    data = load_data()
    entries = []
    for name, info in data.items():
        entries.append({
            "name": name,
            "username": info.get("username", ""),
            "password": info.get("password", ""),
            "strength": info.get("strength", "Unknown"),
        })
    return jsonify(entries)


@app.route("/api/passwords", methods=["POST"])
def add_password():
    payload = request.get_json(force=True)
    name = (payload.get("name") or "").strip()
    username = (payload.get("username") or "").strip()
    password = (payload.get("password") or "").strip()

    if not name:
        return jsonify({"error": "Name is required"}), 400
    if not username:
        return jsonify({"error": "Username is required"}), 400
    if not password:
        return jsonify({"error": "Password is required"}), 400

    data = load_data()
    for key in data:
        if key.lower() == name.lower():
            return jsonify({"error": f"Entry '{key}' already exists. Use update instead."}), 409

    data[name] = {
        "username": username,
        "password": password,
        "strength": check_strength(password),
    }
    save_data(data)
    return jsonify({"message": f"Saved '{name}'", "strength": data[name]["strength"]}), 201


@app.route("/api/passwords/<path:name>", methods=["PUT"])
def update_password(name):
    payload = request.get_json(force=True)
    new_password = (payload.get("password") or "").strip()

    if not new_password:
        return jsonify({"error": "Password is required"}), 400

    data = load_data()
    key = _find_key(data, name)
    if key is None:
        return jsonify({"error": f"No entry found for '{name}'"}), 404

    data[key]["password"] = new_password
    data[key]["strength"] = check_strength(new_password)
    save_data(data)
    return jsonify({"message": f"Updated '{key}'", "strength": data[key]["strength"]})


@app.route("/api/passwords/<path:name>", methods=["DELETE"])
def delete_password(name):
    data = load_data()
    key = _find_key(data, name)
    if key is None:
        return jsonify({"error": f"No entry found for '{name}'"}), 404

    del data[key]
    save_data(data)
    return jsonify({"message": f"Deleted '{key}'"})


@app.route("/api/generate", methods=["POST"])
def api_generate():
    payload = request.get_json(silent=True) or {}
    length = payload.get("length", 16)
    try:
        length = int(length)
    except (TypeError, ValueError):
        length = 16
    length = max(4, min(length, 64))

    password = generate_password(length)
    return jsonify({"password": password, "strength": check_strength(password)})


def _find_key(data, name):
    for key in data:
        if key.lower() == name.lower():
            return key
    return None


if __name__ == "__main__":
    app.run(debug=True, port=5000)
