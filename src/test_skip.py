import pytest

from functions import square, cube

@pytest.mark.skip
def test_square_skip():
    num = 5
    result = square(num)
    assert result == num ** 2

def test_cube():
    """
    Unit test for cube function
    """
    pytest.skip() # skip test during execution
    num = 3
    result = cube(num)
    assert result == num ** 3
