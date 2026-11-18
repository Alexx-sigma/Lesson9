import pytest
from quality_lab.database import Database


def test_database_stores_product():
    db = Database(":memory:")
    try:
        db.add_product("Book", 10)
        assert db.list_products() == [("Book", 10.0)]
    finally:
        db.close()


def test_database_rejects_negative_price():
    db = Database(":memory:")
    try:
        with pytest.raises(ValueError):
            db.add_product("Book", -1)
        assert db.list_products() == []
    finally:
        db.close()


def test_database_rejects_empty_name():
    db = Database(":memory:")
    try:
        with pytest.raises(ValueError):
            db.add_product("   ", 10)
    finally:
        db.close()


def test_database_sql_injection_text_stored_as_data():
    db = Database(":memory:")
    try:
        evil = "x'); DROP TABLE products;--"
        db.add_product(evil, 1)
        assert db.list_products() == [(evil, 1.0)]
    finally:
        db.close()


def test_database_uses_tmp_path_not_production(tmp_path):
    path = tmp_path / "test.sqlite3"
    db = Database(path)
    db.add_product("Book", 10)
    db.close()
    assert path.exists()
