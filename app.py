from flask import Flask, request, render_template, abort
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "users.db"


DB_PASSWORD = os.environ.get("DB_PASSWORD", "defaultpassword")


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cur.executemany("INSERT INTO users (username, password) VALUES (?, ?)", [
        ("alice", "password123"),
        ("bob", "qwerty"),
        ("admin", "admin123"),
    ])
    conn.commit()
    conn.close()

@app.route("/init-db")
def setup():
    init_db()
    return "Database initialized with sample users!"

@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "img-src 'self'; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "frame-ancestors 'none';"
    )
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    response.headers['Server'] = 'MyApp'
    return response


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    q = request.args.get("q", "")
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    query = "SELECT username FROM users WHERE username LIKE ?"
    try:
        cur.execute(query, (f"%{q}%",))  # Safe parameterized query
        results = cur.fetchall()
    except Exception as e:
        results = [("Error", str(e))]
    conn.close()
    return {"results": results}

@app.route("/greet")
def greet():
    name = request.args.get("name", "Guest")
    allowed_names = {"Alice", "Bob", "Charlie", "Guest"}  # Allow-list
    if name not in allowed_names:
        abort(400, "Invalid name")
    return render_template("greeting.html", name=name)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Debug must be False in production
    app.run(host="0.0.0.0", port=port, debug=False)
