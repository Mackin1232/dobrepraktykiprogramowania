import pytest
from logika import funkcje

class TestClass:

    def test_kajak(self):
        assert funkcje.is_palindrome("kajak") == True

    def test_kobyla(self):
        assert funkcje.is_palindrome("Kobyła ma mały bok") == True

    def test_python(self):
        assert funkcje.is_palindrome("python") == False

    def test_puste(self):
        assert funkcje.is_palindrome("") == True

    def test_A(self):
        assert funkcje.is_palindrome("A") == True