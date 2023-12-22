import pytest
import random

from functions import square

@pytest.mark.parametrize("num", [random.randint(1, 10)])
def test_square_param(num):
    result = square(num)
    assert result == num ** 2
