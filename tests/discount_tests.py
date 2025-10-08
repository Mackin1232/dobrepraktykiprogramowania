import pytest

def calculate_discount(price: float, discount: float) -> float:
    if discount < 0 or discount > 1:
        raise ValueError("Zniżka powinna się mieścić w zakresie 0-1")
    return price - (price*discount)

class TestClass:
    def test_100_20(self):
        assert calculate_discount(100,0.2) == 80.0
    def test_50_0(self):
        assert calculate_discount(50,0) == 50.0
    def test_200_100(self):
        assert calculate_discount(200,1) == 0.0
    def test_negative(self):
        with pytest.raises(ValueError):
            calculate_discount(100,-0.1)
    def test_discount_too_high(self):
        with pytest.raises(ValueError):
            calculate_discount(100,1.5)