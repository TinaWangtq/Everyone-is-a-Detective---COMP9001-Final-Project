"""
app.py — Flask web server for "Everyone is a Detective"
========================================================
Thin web layer. All game logic lives in game.py.

Run with:
    pip install flask
    python app.py
Then open http://localhost:5000 in your browser.
"""

from flask import Flask, render_template, request, jsonify, session
import os

from game import GameSession, VALID_GENDERS
from plot import IMAGE_MAP, AUDIO_MAP

app = Flask(__name__)
app.secret_key = "ravenwood-manor-1889-change-me-in-production"


def get_current_session():
    sid = session.get("session_id")
    if not sid:
        return None
    try:
        return GameSession.get(sid)
    except KeyError:
        session.pop("session_id", None)
        return None


def require_session():
    gs = get_current_session()
    if gs is None:
        return None, (jsonify({"error": "No active game. Please start a new one."}), 400)
    return gs, None


@app.route("/")
def home():
    return render_template(
        "index.html",
        genders=VALID_GENDERS,
        image_map=IMAGE_MAP,
        audio_map=AUDIO_MAP,
    )


@app.route("/api/start", methods=["POST"])
def api_start():
    data = request.get_json(force=True) or {}
    try:
        gs = GameSession.create(data.get("name", ""), data.get("gender", ""))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    session["session_id"] = gs.id
    return jsonify({
        "session_id": gs.id,
        "prologue": gs.get_prologue(),
        "state": gs.get_state(),
    })


@app.route("/api/state", methods=["GET"])
def api_state():
    gs, err = require_session()
    if err: return err
    return jsonify(gs.get_state())


@app.route("/api/question", methods=["POST"])
def api_question():
    gs, err = require_session()
    if err: return err
    data = request.get_json(force=True) or {}
    try:
        answer = gs.ask_suspect(data["suspect"], data["question"])
    except KeyError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"answer": answer, "state": gs.get_state()})


@app.route("/api/examine", methods=["POST"])
def api_examine():
    gs, err = require_session()
    if err: return err
    data = request.get_json(force=True) or {}
    try:
        item = gs.examine_item(data["item"])
    except KeyError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({
        "item": {
            "name": data["item"],
            "image": item["image"],
            "description": item["description"],
        },
        "state": gs.get_state(),
    })


@app.route("/api/thought", methods=["POST"])
def api_thought():
    gs, err = require_session()
    if err: return err
    data = request.get_json(force=True) or {}
    ok = gs.add_thought(data.get("text", ""))
    return jsonify({"ok": ok, "state": gs.get_state()})


@app.route("/api/notebook_file", methods=["GET"])
def api_notebook_file():
    gs, err = require_session()
    if err: return err
    return jsonify({"contents": gs.notebook.read_from_file()})


@app.route("/api/accuse", methods=["POST"])
def api_accuse():
    gs, err = require_session()
    if err: return err
    data = request.get_json(force=True) or {}
    try:
        result = gs.make_accusation(data["culprit"], data["evidence"])
    except (KeyError, RuntimeError) as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"result": result, "state": gs.get_state()})


@app.route("/api/reset", methods=["POST"])
def api_reset():
    session.pop("session_id", None)
    return jsonify({"ok": True})


@app.route("/api/assets", methods=["GET"])
def api_assets():
    """Tell the client which expected asset files actually exist."""
    base = app.static_folder

    def exists(rel):
        return os.path.isfile(os.path.join(base, rel))

    return jsonify({
        "images": {k: exists(os.path.join("images", v))
                   for k, v in IMAGE_MAP.items()},
        "audio":  {k: exists(os.path.join("audio", v))
                   for k, v in AUDIO_MAP.items()},
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
