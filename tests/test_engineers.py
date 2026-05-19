import pytest
from app.database import initialise_db
from app import engineers
import os


@pytest.fixture(autouse=True)
def setup_test_db(tmp_path, monkeypatch):
    """Use a temporary database for each test so they don't affect each other."""
    test_db = str(tmp_path / "test.db")
    monkeypatch.setattr("app.database.DB_NAME", test_db)
    monkeypatch.setattr("app.engineers.get_connection", lambda: __import__('sqlite3').connect(test_db))
    initialise_db()


def test_add_engineer():
    """Test that an engineer can be added successfully."""
    engineers.add_engineer("Paul Ciurean", "paul@rebura.com", "07123456789")
    result = engineers.get_all_engineers()
    assert len(result) == 1
    assert result[0]["name"] == "Paul Ciurean"
    assert result[0]["email"] == "paul@rebura.com"


def test_add_engineer_without_phone():
    """Test that an engineer can be added without a phone number."""
    engineers.add_engineer("Jane Doe", "jane@rebura.com")
    result = engineers.get_all_engineers()
    assert result[0]["phone"] is None


def test_get_all_engineers_sorted_by_name():
    """Test that engineers are returned sorted alphabetically by name."""
    engineers.add_engineer("Zara Smith", "zara@rebura.com")
    engineers.add_engineer("Aaron Jones", "aaron@rebura.com")
    result = engineers.get_all_engineers()
    assert result[0]["name"] == "Aaron Jones"
    assert result[1]["name"] == "Zara Smith"


def test_get_engineer_by_id():
    """Test retrieving a single engineer by their ID."""
    engineers.add_engineer("Paul Ciurean", "paul@rebura.com")
    all_engineers = engineers.get_all_engineers()
    engineer_id = all_engineers[0]["id"]
    result = engineers.get_engineer_by_id(engineer_id)
    assert result["name"] == "Paul Ciurean"


def test_get_engineer_by_invalid_id():
    """Test that a non-existent ID returns None."""
    result = engineers.get_engineer_by_id(999)
    assert result is None


def test_update_engineer():
    """Test that an engineer's details can be updated."""
    engineers.add_engineer("Paul Ciurean", "paul@rebura.com")
    all_engineers = engineers.get_all_engineers()
    engineer_id = all_engineers[0]["id"]
    engineers.update_engineer(engineer_id, "Paul Updated", "updated@rebura.com", "07999999999")
    result = engineers.get_engineer_by_id(engineer_id)
    assert result["name"] == "Paul Updated"
    assert result["email"] == "updated@rebura.com"


def test_delete_engineer():
    """Test that an engineer can be deleted."""
    engineers.add_engineer("Paul Ciurean", "paul@rebura.com")
    all_engineers = engineers.get_all_engineers()
    engineer_id = all_engineers[0]["id"]
    engineers.delete_engineer(engineer_id)
    result = engineers.get_engineer_by_id(engineer_id)
    assert result is None


def test_search_engineers_by_name():
    """Test searching for engineers by partial name match."""
    engineers.add_engineer("Paul Ciurean", "paul@rebura.com")
    engineers.add_engineer("Jane Doe", "jane@rebura.com")
    results = engineers.search_engineers_by_name("Paul")
    assert len(results) == 1
    assert results[0]["name"] == "Paul Ciurean"


def test_search_engineers_no_match():
    """Test that searching with no match returns an empty list."""
    engineers.add_engineer("Paul Ciurean", "paul@rebura.com")
    results = engineers.search_engineers_by_name("Nonexistent")
    assert len(results) == 0