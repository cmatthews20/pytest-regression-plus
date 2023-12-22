import pytest
import random
from functions import square

@pytest.fixture
def rand_val():
    return random.randint(1, 10)

def test_square_param(rand_val):
    result = square(rand_val)
    assert result == rand_val ** 2
