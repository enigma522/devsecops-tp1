import pytest
from app import app, init_db, DB_NAME
import sqlite3

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_init_db(client):
    """Test that the database initializes correctly"""
    response = client.get("/init-db")
    assert response.status_code == 200
    assert b"Database initialized" in response.data

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT username FROM users")
    users = [row[0] for row in cur.fetchall()]
    conn.close()
    assert "alice" in users
    assert "bob" in users
    assert "admin" in users

def test_search(client):
    """Test the search endpoint"""
    init_db()  # Ensure DB is initialized
    response = client.get("/search?q=alice")
    assert response.status_code == 200
    data = response.get_json()
    results = [row[0] for row in data["results"]]
    assert "alice" in results
    assert "bob" not in results

    # Test empty search
    response = client.get("/search?q=")
    data = response.get_json()
    all_users = [row[0] for row in data["results"]]
    assert set(all_users) >= {"alice", "bob", "admin"}

def test_greet(client):
    response = client.get("/greet?name=Alice")
    assert response.status_code == 200
    assert b"Hello Alice!" in response.data

    response = client.get("/greet")
    assert b"Hello Guest!" in response.data
