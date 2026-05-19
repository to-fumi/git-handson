import pytest

from src.apps.supermarket import (
    add_tax,
    apply_discount,
    calculate_change,
    total_price,
    unit_price,
)


def test_total_price() -> None:
    assert total_price(150, 3) == 450
    assert total_price(198, 1) == 198


def test_apply_discount() -> None:
    assert apply_discount(1000, 0.1) == 900.0
    assert apply_discount(500, 0.2) == 400.0


def test_add_tax() -> None:
    assert add_tax(1000, 0.1) == 1100.0
    assert add_tax(200, 0.08) == 216.0


def test_calculate_change() -> None:
    assert calculate_change(1000, 750) == 250
    assert calculate_change(500, 500) == 0


def test_unit_price() -> None:
    assert unit_price(300, 3) == 100.0
    assert unit_price(198, 2) == 99.0


def test_unit_price_zero_quantity() -> None:
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        unit_price(300, 0)
