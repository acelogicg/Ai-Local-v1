import json, uuid, sqlite3
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# --- CONFIG ---
with open("config.json") as f:
    config = json.load(f)

# --- MODEL LOAD ---
print(f"Loading model: {config['model_name']}")
load_args = {"device_map": "auto"}
if config.get("quantization") == "4bit":
    load_args["load_in_4bit"] = True
if config.get("torch_dtype"):
    load_args["torch_dtype"] = getattr(torch, config["torch_dtype"])

tokenizer = AutoTokenizer.from_pretrained(config["model_name"])
model = AutoModelForCausalLM.from_pretrained(config["model_name"], **load_args)

# --- FLASK + SQLITE ---
app = Flask(__name__)
CORS(app)  # ✅ aktifkan CORS global

conn = sqlite3.connect("chat_history.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS conversations (
    id TEXT PRIMARY KEY,
    title TEXT,
    created_at TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    conversation_id TEXT,
    timestamp TEXT,
    role TEXT,
    content TEXT,
    FOREIGN KEY(conversation_id) REFERENCES conversations(id)
)
""")
conn.commit()


# --- DATABASE FUNCTIONS ---
def create_conversation(title="New Chat"):
    cid = str(uuid.uuid4())
    cur.execute(
        "INSERT INTO conversations VALUES (?, ?, ?)",
        (cid, title, datetime.utcnow().isoformat())
    )
    conn.commit()
    return cid


def add_message(cid, role, text):
    cur.execute(
        "INSERT INTO messages VALUES (?, ?, ?, ?, ?)",
        (str(uuid.uuid4()), cid, datetime.utcnow().isoformat(), role, text)
    )
    conn.commit()


def get_context(cid, limit):
    cur.execute(
        "SELECT role, content FROM messages WHERE conversation_id=? "
        "ORDER BY timestamp DESC LIMIT ?", (cid, limit)
    )
    rows = cur.fetchall()
    return list(reversed(rows))


# --- ROUTES ---
@app.route("/newchat", methods=["POST"])
def newchat():
    data = request.get_json(force=True)
    cid = create_conversation(data.get("title", "New Chat"))
    return jsonify({"conversation_id": cid})


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    cid = data.get("conversation_id")
    if not cid:
        return jsonify({"error": "conversation_id required"}), 400

    prompt = data.get("prompt", "")
    context = get_context(cid, config["context_limit"])

    full_prompt = ""
    for r, m in context:
        full_prompt += ("User: " if r == "user" else "AI: ") + m.strip() + "\n"
    full_prompt += "User: " + prompt + "\nAI:"

    inputs = tokenizer(full_prompt, return_tensors="pt").to(config["device"])
    output = model.generate(**inputs, max_new_tokens=config["max_new_tokens"])
    reply = tokenizer.decode(output[0], skip_special_tokens=True)

    add_message(cid, "user", prompt)
    add_message(cid, "ai", reply)

    return jsonify({"conversation_id": cid, "response": reply})


@app.route("/conversations", methods=["GET"])
def list_convs():
    cur.execute("SELECT id, title, created_at FROM conversations ORDER BY created_at DESC")
    rows = cur.fetchall()
    return jsonify([
        {"conversation_id": i, "title": t, "created_at": c} for i, t, c in rows
    ])


@app.route("/history/<cid>", methods=["GET"])
def history(cid):
    cur.execute(
        "SELECT role, content, timestamp FROM messages "
        "WHERE conversation_id=? ORDER BY timestamp ASC", (cid,)
    )
    rows = cur.fetchall()
    if not rows:
        return jsonify({"error": "conversation not found"}), 404
    return jsonify({
        "conversation_id": cid,
        "messages": [{"role": r, "content": m, "timestamp": t} for r, m, t in rows]
    })


# --- MAIN ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
