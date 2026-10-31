import sqlite3
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
DB = "todo.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    conn = sqlite3.connect(DB)
    rows = conn.execute("SELECT id, title, done FROM tasks").fetchall()
    conn.close()
    return jsonify([{"id": r[0], "title": r[1], "done": bool(r[2])} for r in rows])

@app.route("/api/tasks", methods=["POST"])
def add_task():
    title = request.json.get("title", "").strip()
    if not title:
        return jsonify({"error": "empty title"}), 400
    conn = sqlite3.connect(DB)
    cur = conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    conn.commit()
    task_id = cur.lastrowid
    conn.close()
    return jsonify({"id": task_id, "title": title, "done": False}), 201

@app.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def toggle_task(task_id):
    conn = sqlite3.connect(DB)
    conn.execute("UPDATE tasks SET done = 1 - done WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = sqlite3.connect(DB)
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
