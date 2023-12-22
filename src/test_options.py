import pytest
from functions import square, cube

def test_square():
    num = 5
    result = square(num)
    assert result == num ** 2

def test_cube():
    num = 3
    result = cube(num)
    assert result == num ** 3
