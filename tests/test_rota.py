import pytest
from app.database import initialise_db
from app import engineers, rota


@pytest.fixture(autouse=True)
def setup_test_db(tmp_path, monkeypatch):
    """Use a temporary database for each test."""
    test_db = str(tmp_path / "test.db")
    monkeypatch.setattr("app.database.DB_NAME", test_db)
    monkeypatch.setattr("app.engineers.get_connection", lambda: __import__('sqlite3').connect(test_db))
    monkeypatch.setattr("app.rota.get_connection", lambda: __import__('sqlite3').connect(test_db))
    initialise_db()


@pytest.fixture
def sample_engineer(tmp_path, monkeypatch):
    """Create a sample engineer and return their ID."""
    engineers.add_engineer("Paul Ciurean", "paul@rebura.com")
    all_engineers = engineers.get_all_engineers()
    return all_engineers[0]["id"]


def test_assign_rota(sample_engineer):
    """Test that a rota entry can be assigned to an engineer."""
    rota.assign_rota(sample_engineer, "2026-05-01", "2026-05-07", "day")
    result = rota.get_full_rota()
    assert len(result) == 1
    assert result[0]["name"] == "Paul Ciurean"
    assert result[0]["shift"] == "day"


def test_get_full_rota_sorted_by_date(sample_engineer):
    """Test that the full rota is returned sorted by start date."""
    rota.assign_rota(sample_engineer, "2026-06-01", "2026-06-07", "day")
    rota.assign_rota(sample_engineer, "2026-05-01", "2026-05-07", "night")
    result = rota.get_full_rota()
    assert result[0]["start_date"] == "2026-05-01"
    assert result[1]["start_date"] == "2026-06-01"


def test_get_rota_by_date_within_range(sample_engineer):
    """Test that querying a date within a rota range returns the correct engineer."""
    rota.assign_rota(sample_engineer, "2026-05-20", "2026-05-27", "day")
    results = rota.get_rota_by_date("2026-05-23")
    assert len(results) == 1
    assert results[0]["name"] == "Paul Ciurean"


def test_get_rota_by_date_outside_range(sample_engineer):
    """Test that querying a date outside all rota ranges returns nothing."""
    rota.assign_rota(sample_engineer, "2026-05-20", "2026-05-27", "day")
    results = rota.get_rota_by_date("2026-06-01")
    assert len(results) == 0


def test_get_rota_by_date_on_start_date(sample_engineer):
    """Test that querying the exact start date returns the correct entry."""
    rota.assign_rota(sample_engineer, "2026-05-20", "2026-05-27", "day")
    results = rota.get_rota_by_date("2026-05-20")
    assert len(results) == 1


def test_get_rota_by_date_on_end_date(sample_engineer):
    """Test that querying the exact end date returns the correct entry."""
    rota.assign_rota(sample_engineer, "2026-05-20", "2026-05-27", "day")
    results = rota.get_rota_by_date("2026-05-27")
    assert len(results) == 1


def test_get_rota_by_engineer(sample_engineer):
    """Test retrieving all rota entries for a specific engineer."""
    rota.assign_rota(sample_engineer, "2026-05-01", "2026-05-07", "day")
    rota.assign_rota(sample_engineer, "2026-06-01", "2026-06-07", "night")
    results = rota.get_rota_by_engineer(sample_engineer)
    assert len(results) == 2


def test_delete_rota_entry(sample_engineer):
    """Test that a rota entry can be deleted."""
    rota.assign_rota(sample_engineer, "2026-05-01", "2026-05-07", "day")
    full_rota = rota.get_full_rota()
    rota_id = full_rota[0]["id"]
    rota.delete_rota_entry(rota_id)
    result = rota.get_full_rota()
    assert len(result) == 0