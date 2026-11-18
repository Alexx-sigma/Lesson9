import pytest
from quality_lab.parser import parse_products
from quality_lab.exceptions import BotDataError


def test_parser_fake_response_without_internet():
    fake_fetch = lambda: {"products": [{"name": "Book", "price": 10}]}
    assert parse_products(fake_fetch) == [{"name": "Book", "price": 10}]


def test_parser_rejects_missing_key():
    with pytest.raises(BotDataError):
        parse_products(lambda: {})


def test_parser_empty_list():
    assert parse_products(lambda: {"products": []}) == []


@pytest.mark.parametrize("bad", [
    {"products": [{"name": "Book", "price": -1}]},
    {"products": [{"name": "Book", "price": "10"}]},
    {"products": [{"name": "Book", "price": True}]},
    {"products": [{"price": 5}]},
    {"products": ["Book"]},
    {"products": None},
])
def test_parser_malformed_values(bad):
    with pytest.raises(BotDataError):
        parse_products(lambda: bad)


def test_parser_source_exception_is_wrapped():
    def broken():
        raise ConnectionError("no network")
    with pytest.raises(BotDataError):
        parse_products(broken)


def test_parser_with_monkeypatch_fake_data(monkeypatch):
    """monkeypatch подменяет «сетевую» функцию фейковыми данными — интернет не нужен."""
    import quality_lab.parser as parser_module

    def fake_fetch():
        return {"products": [{"name": "Tea", "price": 3.5}]}

    monkeypatch.setattr(parser_module, "fetch_products", fake_fetch, raising=False)
    assert parser_module.parse_products(parser_module.fetch_products) == [{"name": "Tea", "price": 3.5}]


def test_parser_does_not_log_secrets(monkeypatch, caplog):
    def broken():
        raise RuntimeError("token=SECRET123")
    with caplog.at_level("INFO"):
        with pytest.raises(BotDataError):
            parse_products(broken)
    assert "SECRET123" not in caplog.text
