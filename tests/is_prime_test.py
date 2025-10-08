import math
from logika import funkcje

class TestClass:
    def test_2(self):
        assert funkcje.is_prime(2) == True
    def test_3(self):
        assert funkcje.is_prime(3) == True
    def test_4(self):
        assert funkcje.is_prime(4) == False
    def test_0(self):
        assert funkcje.is_prime(0) == False
    def test_1(self):
        assert funkcje.is_prime(1) == False
    def test_5(self):
        assert funkcje.is_prime(5) == True
    def test_97(self):
        assert funkcje.is_prime(97) == True