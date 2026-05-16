from app.database import get_connection


def assign_rota(engineer_id, start_date, end_date, shift):
    """Assign an engineer to an on-call slot with a date range."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO rota (engineer_id, start_date, end_date, shift) VALUES (?, ?, ?, ?)",
        (engineer_id, start_date, end_date, shift)
    )
    conn.commit()
    conn.close()


def get_full_rota():
    """Return the full rota with engineer names, sorted by start date."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT rota.id, engineers.name, rota.start_date, rota.end_date, rota.shift
        FROM rota
        JOIN engineers ON rota.engineer_id = engineers.id
        ORDER BY rota.start_date ASC
    """)
    rota = cursor.fetchall()
    conn.close()
    return rota


def get_rota_by_date(query_date):
    """Return all rota entries where the query date falls within the start and end date range."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT rota.id, engineers.name, rota.start_date, rota.end_date, rota.shift
        FROM rota
        JOIN engineers ON rota.engineer_id = engineers.id
        WHERE ? BETWEEN rota.start_date AND rota.end_date
        ORDER BY rota.shift ASC
    """, (query_date,))
    results = cursor.fetchall()
    conn.close()
    return results


def get_rota_by_engineer(engineer_id):
    """Return all rota entries for a specific engineer."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT rota.id, engineers.name, rota.start_date, rota.end_date, rota.shift
        FROM rota
        JOIN engineers ON rota.engineer_id = engineers.id
        WHERE rota.engineer_id = ?
        ORDER BY rota.start_date ASC
    """, (engineer_id,))
    results = cursor.fetchall()
    conn.close()
    return results


def delete_rota_entry(rota_id):
    """Remove a rota entry by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rota WHERE id = ?", (rota_id,))
    conn.commit()
    conn.close()
