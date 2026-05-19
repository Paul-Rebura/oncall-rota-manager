from app.database import get_connection


def add_engineer(name, email, phone=None):
    """Add a new engineer to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO engineers (name, email, phone) VALUES (?, ?, ?)",
        (name, email, phone)
    )
    conn.commit()
    conn.close()


def get_all_engineers():
    """Return a list of all engineers, sorted by name."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM engineers ORDER BY name ASC")
    engineers = cursor.fetchall()
    conn.close()
    return engineers


def get_engineer_by_id(engineer_id):
    """Return a single engineer by their ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM engineers WHERE id = ?", (engineer_id,))
    engineer = cursor.fetchone()
    conn.close()
    return engineer


def update_engineer(engineer_id, name, email, phone=None):
    """Update an existing engineer's details."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE engineers SET name = ?, email = ?, phone = ? WHERE id = ?",
        (name, email, phone, engineer_id)
    )
    conn.commit()
    conn.close()


def delete_engineer(engineer_id):
    """Delete an engineer by their ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM engineers WHERE id = ?", (engineer_id,))
    conn.commit()
    conn.close()


def search_engineers_by_name(search_term):
    """Search for engineers whose name contains the search term."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM engineers WHERE name LIKE ?",
        (f"%{search_term}%",)
    )
    results = cursor.fetchall()
    conn.close()
    return results
