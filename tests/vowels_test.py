import pytest

def count_vowels(text: str) -> int:
    counter = 0
    vowels = ["a", "e", "i", "o", "u", "y", "ą", "ę", "ó"]
    text = text.lower()
    for letter in text:
        if letter in vowels:
            counter += 1
    return counter

class TestClass:
    def test_python(self):
        assert count_vowels("Python") == 2
    def test_aeiouy(self):
        assert count_vowels("AEIOUY") == 6
    def test_bcd(self):
        assert count_vowels("bcd") == 0
    def test_blank(self):
        assert count_vowels("") == 0
    def test_zolw(self):
        assert count_vowels("Próba żółwia") == 5
