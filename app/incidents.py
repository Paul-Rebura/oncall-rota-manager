from app.database import get_connection
from datetime import datetime


def log_incident(rota_id, title, severity, description=None):
    """Log a new incident against a rota entry."""
    raised_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO incidents (rota_id, title, severity, description, raised_at)
           VALUES (?, ?, ?, ?, ?)""",
        (rota_id, title, severity, description, raised_at)
    )
    conn.commit()
    conn.close()


def get_all_incidents():
    """Return all incidents with linked rota and engineer info, sorted by date."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT incidents.id, engineers.name, incidents.title,
               incidents.severity, incidents.raised_at, incidents.resolved
        FROM incidents
        JOIN rota ON incidents.rota_id = rota.id
        JOIN engineers ON rota.engineer_id = engineers.id
        ORDER BY incidents.raised_at DESC
    """)
    incidents = cursor.fetchall()
    conn.close()
    return incidents


def get_incidents_by_severity(severity):
    """Return all incidents filtered by severity level."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT incidents.id, engineers.name, incidents.title,
               incidents.severity, incidents.raised_at, incidents.resolved
        FROM incidents
        JOIN rota ON incidents.rota_id = rota.id
        JOIN engineers ON rota.engineer_id = engineers.id
        WHERE incidents.severity = ?
        ORDER BY incidents.raised_at DESC
    """, (severity,))
    results = cursor.fetchall()
    conn.close()
    return results


def resolve_incident(incident_id):
    """Mark an incident as resolved."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE incidents SET resolved = 1 WHERE id = ?",
        (incident_id,)
    )
    conn.commit()
    conn.close()


def sort_incidents_by_severity(incidents):
    """Sort a list of incidents by severity using a custom order (bubble sort)."""
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    n = len(incidents)
    incidents = list(incidents)
    for i in range(n):
        for j in range(0, n - i - 1):
            if severity_order[incidents[j]["severity"]] > severity_order[incidents[j + 1]["severity"]]:
                incidents[j], incidents[j + 1] = incidents[j + 1], incidents[j]
    return incidents
