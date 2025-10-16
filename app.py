from flask import Flask, request, render_template, render_template_string
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "users.db"

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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    q = request.args.get("q", "")
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    query = "SELECT username FROM users WHERE username LIKE ?"
    print("Executing:", query, "with param:", f"%{q}%")
    try:
        cur.execute(query, (f"%{q}%",))  
        results = cur.fetchall()
    except Exception as e:
        results = [("Error", str(e))]
    conn.close()
    return {"results": results}


# @app.route("/search")
# def search():
#     q = request.args.get("q", "")
#     conn = sqlite3.connect(DB_NAME)
#     cur = conn.cursor()
#     query = f"SELECT username FROM users WHERE username LIKE '%{q}%'"
#     print("Executing:", query)
#     try:
#         cur.execute(query)
#         results = cur.fetchall()
#     except Exception as e:
#         results = [("Error", str(e))]
#     conn.close()
#     return {"results": results}


@app.route("/greet")
def greet():
    name = request.args.get("name", "Guest")
    return render_template("greeting.html", name=name)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
