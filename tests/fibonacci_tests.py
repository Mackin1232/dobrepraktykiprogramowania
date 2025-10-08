import pytest

def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 2) + fibonacci(n - 1)

class TestClass:
    def test_0(self):
        assert fibonacci(0) == 0

    def test_1(self):
        assert fibonacci(1) == 1

    def test_5(self):
        assert fibonacci(5) == 5

    def test_10(self):
        assert fibonacci(10) == 55

    def test_negative(self):
        with pytest.raises(ValueError):
            fibonacci(-1)

