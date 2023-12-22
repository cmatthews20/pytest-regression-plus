import pytest
import random
from functions import square

@pytest.fixture(scope="session")
def rand_val():
    rand_int = random.randint(1, 10)
    return rand_int

def test_square_param(rand_val):
    result = square(rand_val)
    assert result == rand_val ** 2
