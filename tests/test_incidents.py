import pytest
from app.database import initialise_db
from app import engineers, rota, incidents


@pytest.fixture(autouse=True)
def setup_test_db(tmp_path, monkeypatch):
    """Use a temporary database for each test."""
    test_db = str(tmp_path / "test.db")
    monkeypatch.setattr("app.database.DB_NAME", test_db)
    monkeypatch.setattr("app.engineers.get_connection", lambda: __import__('sqlite3').connect(test_db))
    monkeypatch.setattr("app.rota.get_connection", lambda: __import__('sqlite3').connect(test_db))
    monkeypatch.setattr("app.incidents.get_connection", lambda: __import__('sqlite3').connect(test_db))
    initialise_db()


@pytest.fixture
def sample_rota_id(tmp_path, monkeypatch):
    """Create a sample engineer and rota entry, return the rota ID."""
    engineers.add_engineer("Paul Ciurean", "paul@rebura.com")
    all_engineers = engineers.get_all_engineers()
    engineer_id = all_engineers[0]["id"]
    rota.assign_rota(engineer_id, "2026-05-01", "2026-05-07", "day")
    full_rota = rota.get_full_rota()
    return full_rota[0]["id"]


def test_log_incident(sample_rota_id):
    """Test that an incident can be logged against a rota entry."""
    incidents.log_incident(sample_rota_id, "EC2 instance unreachable", "high", "Instance stopped responding")
    result = incidents.get_all_incidents()
    assert len(result) == 1
    assert result[0]["title"] == "EC2 instance unreachable"
    assert result[0]["severity"] == "high"


def test_log_incident_without_description(sample_rota_id):
    """Test that an incident can be logged without a description."""
    incidents.log_incident(sample_rota_id, "S3 bucket access denied", "medium")
    result = incidents.get_all_incidents()
    assert len(result) == 1
    assert result[0]["title"] == "S3 bucket access denied"


def test_get_incidents_by_severity(sample_rota_id):
    """Test filtering incidents by severity level."""
    incidents.log_incident(sample_rota_id, "EC2 instance unreachable", "high")
    incidents.log_incident(sample_rota_id, "S3 bucket access denied", "medium")
    results = incidents.get_incidents_by_severity("high")
    assert len(results) == 1
    assert results[0]["severity"] == "high"


def test_resolve_incident(sample_rota_id):
    """Test that an incident can be marked as resolved."""
    incidents.log_incident(sample_rota_id, "EC2 instance unreachable", "high")
    all_incidents = incidents.get_all_incidents()
    incident_id = all_incidents[0]["id"]
    incidents.resolve_incident(incident_id)
    result = incidents.get_all_incidents()
    assert result[0]["resolved"] == 1


def test_incident_defaults_to_unresolved(sample_rota_id):
    """Test that a newly logged incident is unresolved by default."""
    incidents.log_incident(sample_rota_id, "RDS connection timeout", "critical")
    result = incidents.get_all_incidents()
    assert result[0]["resolved"] == 0


def test_sort_incidents_by_severity(sample_rota_id):
    """Test that the bubble sort correctly orders incidents from critical to low."""
    incidents.log_incident(sample_rota_id, "Low priority alert", "low")
    incidents.log_incident(sample_rota_id, "Critical outage", "critical")
    incidents.log_incident(sample_rota_id, "Medium alert", "medium")
    all_incidents = incidents.get_all_incidents()
    sorted_incidents = incidents.sort_incidents_by_severity(all_incidents)
    assert sorted_incidents[0]["severity"] == "critical"
    assert sorted_incidents[-1]["severity"] == "low"


def test_get_all_incidents_sorted_by_date(sample_rota_id):
    """Test that incidents are returned with the most recent first."""
    incidents.log_incident(sample_rota_id, "First incident", "low")
    incidents.log_incident(sample_rota_id, "Second incident", "high")
    result = incidents.get_all_incidents()
    assert result[0]["title"] == "Second incident"