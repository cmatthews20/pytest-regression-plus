# Unit tests

import time

from functions import square, cube

def test_square():
    """
    Unit test for square function
    """

    num = 5
    result = square(num)
    assert result == num ** 2

def test_cube():
    """
    Unit test for cube function
    """
    
    num = 3
    result = cube(num)
    time.sleep(10)
    assert result == num ** 3
