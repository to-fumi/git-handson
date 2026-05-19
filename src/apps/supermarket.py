import os

from dotenv import load_dotenv

from src.core.calculator import add, divide, multiply, subtract

load_dotenv()

TAX_RATE = float(os.environ["TAX_RATE"])
DISCOUNT_RATE = float(os.environ["DISCOUNT_RATE"])


def total_price(unit_price: float, quantity: int) -> float:
    return multiply(unit_price, quantity)


def apply_discount(price: float, discount_rate: float = DISCOUNT_RATE) -> float:
    return subtract(price, multiply(price, discount_rate))


def add_tax(price: float, tax_rate: float = TAX_RATE) -> float:
    return add(price, multiply(price, tax_rate))


def calculate_change(paid: float, total: float) -> float:
    return subtract(paid, total)


def unit_price(total_price: float, quantity: int) -> float:
    return divide(total_price, quantity)
