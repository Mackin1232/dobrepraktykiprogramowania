import string
from logika import funkcje


class TestClass:
    def test_tobe(self):
        assert funkcje.word_frequencies("To be or not to be") == {"to": 2, "be": 2, "or": 1, "not":1}
    def test_hello(self):
        assert funkcje.word_frequencies("Hello, hello!") == {"hello": 2}
    def test_blank(self):
        assert funkcje.word_frequencies("") == {}
    def test_python(self):
        assert funkcje.word_frequencies("Python Python python") == {"python": 3}
    def test_ala(self):
        assert funkcje.word_frequencies("Ala ma kota, a kot ma Ale.") == {"ala": 1, "ma": 2, "kota": 1, "a": 1, "kot": 1, "ale": 1}
