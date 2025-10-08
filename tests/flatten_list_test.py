import pytest
from logika import funkcje

class TestClass:
    def test_1depth(self):
        assert funkcje.flatten_list([1,2,3]) == [1,2,3]
    def test_3depth(self):
        assert funkcje.flatten_list([1,[2,3],[4,[5]]]) == [1,2,3,4,5]
    def test_empty(self):
        assert funkcje.flatten_list([]) == []
    def test_1element(self):
        assert funkcje.flatten_list([[[1]]]) == [1]
    def test_4depth(self):
        assert funkcje.flatten_list([1, [2, [3, [4]]]]) == [1,2,3,4]