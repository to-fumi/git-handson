import pytest

from src.core.calculator import add, divide, multiply, subtract


def test_add() -> None:
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_subtract() -> None:
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5
    assert subtract(-2, -3) == 1


def test_multiply() -> None:
    assert multiply(3, 4) == 12
    assert multiply(-2, 5) == -10
    assert multiply(0, 100) == 0


def test_divide() -> None:
    assert divide(10, 2) == 5.0
    assert divide(7, 2) == 3.5
    assert divide(-6, 3) == -2.0


def test_divide_by_zero() -> None:
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(1, 0)
