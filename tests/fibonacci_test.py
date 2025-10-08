import pytest
from logika import funkcje

class TestClass:
    def test_0(self):
        assert funkcje.fibonacci(0) == 0

    def test_1(self):
        assert funkcje.fibonacci(1) == 1

    def test_5(self):
        assert funkcje.fibonacci(5) == 5

    def test_10(self):
        assert funkcje.fibonacci(10) == 55
    def test_negative(self):
        with pytest.raises(ValueError):
            funkcje.fibonacci(-1)

