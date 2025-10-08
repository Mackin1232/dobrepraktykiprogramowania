import pytest

def is_palindrome(text: str) -> bool:
    text = text.lower().replace(" ","")
    reversed = text[::-1]
    if reversed == text:
        return True
    return False

class TestClass:
    
    def test_kajak(self):
        assert is_palindrome("kajak") == True

    def test_kobyla(self):
        assert is_palindrome("Kobyła ma mały bok") == True

    def test_python(self):
        assert is_palindrome("python") == False

    def test_puste(self):
        assert is_palindrome("") == True

    def test_A(self):
        assert is_palindrome("A") == True