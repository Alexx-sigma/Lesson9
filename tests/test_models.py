import pytest
from quality_lab.models import Hero, Product


def test_hero_damage_reduces_health():
    hero = Hero("Ada", 100)
    hero.take_damage(20)
    assert hero.health == 80


def test_product_discount():
    product = Product("Book", 100)
    assert product.discounted_price(20) == 80


def test_hero_negative_initial_health_rejected():
    with pytest.raises(ValueError):
        Hero("Ada", -1)


def test_hero_damage_does_not_go_below_zero():
    hero = Hero("Ada", 10)
    hero.take_damage(15)
    assert hero.health == 0


def test_product_negative_price_rejected():
    with pytest.raises(ValueError):
        Product("Book", -5)


@pytest.mark.parametrize("percent,expected", [(0, 100), (100, 0)])
def test_discount_boundaries(percent, expected):
    assert Product("Book", 100).discounted_price(percent) == expected


@pytest.mark.parametrize("percent", [-1, 101])
def test_discount_invalid_percent(percent):
    with pytest.raises(ValueError):
        Product("Book", 100).discounted_price(percent)
