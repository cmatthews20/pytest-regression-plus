import pytest
import random
import numpy as np

@pytest.fixture(scope="session")
def rand_val_10():
    rand_int = random.randint(1, 10)
    return rand_int

@pytest.fixture(scope="session")
def rand_val_20():
    rand_int = random.randint(1, 20)
    return rand_int

@pytest.fixture()
def yield_example():
    print("Providing the value: 1")
    yield 1
    print("Cleaning up test resources...")

@pytest.fixture(autouse=True)
def logging_example():
    print("Test starting")

def pytest_addoption(parser):
    parser.addoption("--num_seeds", action="store", type=int, default=1)
    parser.addoption("--seed", action="store", type=int, default=1)

def pytest_generate_tests(metafunc):
    
    
    if "rand_val" in metafunc.fixturenames:
        list = []
        np.random.seed(seed=metafunc.config.getoption("--seed"))
        for i in range(metafunc.config.getoption("--num_seeds")):
            rand_int = np.random.randint(1,100)
            print(rand_int)
            list.append(rand_int)
            list.sort()
        metafunc.parametrize("rand_val", list)
        