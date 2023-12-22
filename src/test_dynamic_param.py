from functions import square
import time

def test_square_dynamic(rand_val):
    result = square(rand_val)
    print(rand_val)
    time.sleep(1)
    assert result == rand_val ** 2
