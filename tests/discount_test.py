import pytest
from logika import funkcje

class TestClass:
    def test_100_20(self):
        assert funkcje.calculate_discount(100,0.2) == 80.0
    def test_50_0(self):
        assert funkcje.calculate_discount(50,0) == 50.0
    def test_200_100(self):
        assert funkcje.calculate_discount(200,1) == 0.0
    def test_negative(self):
        with pytest.raises(ValueError):
            funkcje.calculate_discount(100,-0.1)
    def test_discount_too_high(self):
        with pytest.raises(ValueError):
            funkcje.calculate_discount(100,1.5)