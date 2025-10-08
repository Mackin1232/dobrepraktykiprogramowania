import pytest
from logika import funkcje

class TestClass:
    def test_python(self):
        assert funkcje.count_vowels("Python") == 2
    def test_aeiouy(self):
        assert funkcje.count_vowels("AEIOUY") == 6
    def test_bcd(self):
        assert funkcje.count_vowels("bcd") == 0
    def test_blank(self):
        assert funkcje.count_vowels("") == 0
    def test_zolw(self):
        assert funkcje.count_vowels("Próba żółwia") == 5
