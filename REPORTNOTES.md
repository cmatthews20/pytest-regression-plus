## 1 - Introduction to Software Testing

```pytest --help```

will want to have second test (cube) to demonstrate test selection more thoroughly.

### Why Write Tests?

Writing software tests is a crucial aspect of the software development process. Tests help catch and identify bugs and issues early in the development process. This makes it easier and more cost-effective to fix problems before they become more complex. Writing tests encourages the developer to write modular, maintainable, and loosely coupled code. This, in turn, leads to higher overall code quality. Tests provide a safety net when making changes or adding new features. Having a comprehensive test suite gives developers confidence that their changes won't introduce unexpected issues. With a solid set of tests, developers can refactor code with greater confidence. They can make changes to the codebase, knowing that if something breaks, the tests will catch it. Tests serve as living documentation for your code. They describe how different parts of your code should behave. This can be especially valuable when onboarding new team members or revisiting code after some time. Automated tests can be rerun quickly and easily, allowing you to perform regression testing whenever changes are made. This helps ensure that existing functionality remains intact after modifications. Tests are an integral part of CI/CD pipelines. They enable automated testing and ensure that only code that passes all tests is deployed, reducing the risk of releasing faulty software. Detecting and fixing bugs early in the development process is less expensive than addressing them later in the software development life cycle or, worse, after the software has been deployed. Tests provide a clear specification of what the code is supposed to do. This can enhance collaboration between team members, as it helps in understanding and validating each other's work. Knowing that a product has a robust set of tests can instill confidence in both development teams and end-users. It indicates a commitment to quality and reliability. Tests make it easier to maintain and update code over time. As requirements change or new features are added, tests act as a safety net, ensuring that existing functionality is not inadvertently broken.

In summary, writing software tests is an investment in the quality and reliability of the software, with benefits at the code, and business level. It leads to more robust, maintainable code and provides numerous benefits throughout the development life cycle. Additionally, the organization may be be following some software development methodology that demands tests from the outset; such as Test Driven Development (TDD).

So, after correctly asserting that tests are required - tests are written, put them in a test suite, and any time someone wants to make changes to the code, they must first run this test suite (and make sure all the tests are still passing). Very important for large and complex software where something may not be caught at manual inspection points such as code review, or via functional/usability quality assurance testing.


### Test Frameworks

Test frameworks enable a developer to design, implement, and execute tests. These frameworks typically provide additional features, as seen below:

A developer does not need to use a testing framework; they can certainly write their own. However, they would be be reinventing the wheel, since a way to run the tests needs to be created. Developers want to spend more time writing tests and software, not making the functionality to run the tests. Regardless of the software, the desire to parallelize, parameterize, randomize, _, or _ often arises. Some of these features are provided by pytest. But what about the ones that are not? That is the purpose of this report. To extend pytest to cover those edge cases, and provide a written, off the shelf framework that can be used.

### Installing pytest

covered in pytest docs (install using pip, see "getting started" page).

```bash
pip install -U pytest
```

### next

tests are within python files. these files must be named a certain way. pytest only searches for tests in files with "test" in the name *by default*. This is also true for function names. Funcs without "test" in the name, will not be considered as tests by the framework. Funcs that are considered to be tests, are actually just end up being run by the framework.

(make a note categorizing the sample tests as unit tests. define unit tests.)

### round 1, funcs and tests

the tests are using a hardcoded number, calling square, getting the result, and comparing against a reference.

### what constitutes a passed test?

if a test gets to the end with no errors, it is considered a pass. note that a failed assert results in an error, and the test is marked as a failed test. this is not the only failure that can arise. calls to functions or any external resource for example would qualify. 

### Running and Selecting Tests

how do we run these tests? selecting tests?

run the pytest executable that was installed previously.

call pytest on the command line without any arguments: by default, starts in working dir, and searches recursively in sub dirs to find available tests, and run all of them.

can also provide a dir, file, or specific test for pytest if you dont want to use the working dir.

```bash
# Run all tests
pytest

# run tests in given directory
pytest ./directory_or_filename

# run a specific test
pytest test_functions.py::test_square
```

substring matching. will deselect all tests that cant match with the string provided after the -k flag. This functionality allows for the implicit categorization of tests by their (function) name.

```bash
# runs one
pytest -k square
``` 

```bash
# runs both
pytest -k test
``` 

### Collecting Tests

Collecting tests is a way to see what tests are available. Appending the `--collect-only` argument/flag to end of pytest command prints (lists) the hierarchy of tests that are available. These tests are not executed - they are collected and shown to the developer.

```bash
pytest --collect-only
```

## 2 Test Classes

previously we were looking at standalone test functions. Standalone tests are prefectly fine - but often it is convenient to group tests together with a function they rely upon and/or related data members. Test classes can also be used simply to group related tests. Therefore, test classes must be considered. A test class would allow us to factor out the 5 from each test function for square and cube. Test classes also must be prefixed with "Test". If the prefix is not there, pytest will not look at the members of the class. Please note that the test classes do not share the exact same space in memory for a shared data member such as `num`. Each test will get its own instance of the data. This is by design. It is not desirable for tests to be interacting with eachother underneath the hood. Tests must remain independent. Test selection works the same with classes as it does with standalone tests.

```bash
pytest test_classes.py::TestClass::test_square_class
```



## 3 skipping tests

Sometimes, a developer may want to skip certain tests. Therefore, it would be convenient if this was enabled at the code level. This would remove the need to customize the pytest commands in order to skip tests. Pytest includes several ways to do this.

One way to skip tests, is with the `@pytest.mark.skip` decorator. Pytest must be imported to do this. After collection, at the execution stage, the decorator indicates to pytest that this test should not be run.

When running test_skip.py, we see that the yellow s in the command line indicates it has been skipped as intended.

Just as this marker can be added to standalone test functions, it can be added to other test structures, such as test classes. The marker can also be applied to test functions within a class to skip certain functions within a class, while allowing the other test functions within the class to run. To avoid redundant code, this will not be demonstrated with classes. The simplest use cases will be demonstrated in order to reduce complexity while moving towards the solution.

Instead of skipping a test prior to execution, there may be cases where tests should be skipped during execution. I.e. a codepath that isnt implemented is reached; instead of failing the test, or issuing a pseudo-pass, it can be skipped by calling/envoking `pytest.skip()`. This will skip the test and mark it accordingly during execution. This differs from the previous method in code as well, since the skip is taking place within the test body, not just as a function/class decorator.

When a test is skipped, it is important to document why a particular test was skipped. This will ensure any developers (including the author) does not return to the codebase wondering why certain tests were skipped. This can be accomplished by passing a `reason` parameter to the skip decorator as seen below:

```python
@pytest.mark.skip(reason="skipped test because...")
```

By default, this reason is now shown in the output when the tests are run. You can specifiy an increased verbosity in the command line by adding the `-rs` flag (s indicating extra info for skipped tests). Passing this flag will print the skip reason when invoking tests.

Unconditionally skipping tests is not sufficient. Utilizing a slightly different decorator grants the possibility of conditionally skipping tests.

```
import sys
import pytest
@pytest.mark.skipif(sys.version_info > (3,6), reason="Test required python version <= 3.6")
...
```

The `skipif` decorator will skip the test if the condition passed evaluates to TRUE. A reason is required for skipif decorators. This is just good practice regardless. 

Tests in a certain file can also be skipped based on the success of a package import. Please see the pytest documentation for more information. This method is not covered, as it does not assist the purpose of the report and is outside of the scope. It does assist overall code quality/robustness, but does not assist the devlopment of parallelized regression tests (for scope we can say that only the relevant features of pytest will be covered to avoid overcomplication, restating the documentation, or involving irrelevant material).

## 4 xfail tests

How to deal with tests that cannot succeed? There may be tests that fail that we still want to execute. I.e. when testing a specific failure codepath (want to make sure the code is doing the correct thing, even in the case of a failure)

***skipped***

## 5 parameterizing tests

This section will introduce the concept of test parameterization in pytest. In previous sections, basic test examples have been used. These tests are referred to as directed tests, because the test inputs were hardcoded into the tests themselves. In directed tests, a hardcoded input is given which should always yield the same output. While this is perfectly suitable for simple tests or functions that are only designed for a single input, often times a developer will need to vary the inputs. Pytest provides this functionality with another decorator. The test seen below will test the square function three times, using numbers one through three for each input.

```python
@pytest.mark.parametrize("num", [1,2,3])
def test_square_param(num):
    result = square(num)
    assert result == num ** 2
```

Multiple parameters can be added at the same time.

```python
@pytest.mark.parametrize("num,ref", [(1,1),(2,4),(3,9)])
def test_square_param(num, ref):
    result = square(num)
    assert result == ref
```


This marks the starting point for incorporating randomized tests into the framework wrapper. Although it would be easy to tell the developer to write randomized tests as seen below, it would not provide any additional value. The aim is to provide a framework for doing so without introducing any hardcoded randomized values while factoring out and centralizing this functionality.

```python
import random

@pytest.mark.parametrize("num", [random.randint(1, 10)])
def test_square_param(num):
    result = square(num)
    assert result == num ** 2
```

Pytest also allows the parametrization of tests where values are independent of one another. In the following case, the inputs are varied independently, essentially computing the cartesian product of the `base` and `exponent` lists, creating all possible combinations as inputs to the test. Although this will not be used further to avoid any overcomplication of the explanation of the framework wrapper, it would be used when testing real software.

```python
import math
import pytest

def pow(base, exponent):
    return base ** exponent


@pytest.mark.parametrize("base", [1, 2, 3])
@pytest.mark.parametrize("exponent", [4, 5, 6])
def test_pow(base, exponent):
    result = pow(base, exponent)
    assert result == math.pow(base, exponent)
```

Markers can be applied to specific variants if needed. Each test variant can also be assigned an identifier string. This is useful for large and complicated test suites or where test inputs may not be intuitive. During collection, each test will be accompanied by its identity. This serves as a form of self-enclosed documentation.

```python
@pytest.mark.parametrize(
    "num",
    [
        pytest.param(-1, id="negative"),
        pytest.param(0, id="zero"),
        pytest.param(1, id="positive"),
    ],
)
def test_square(num):
    result = square(num)
    assert result == num ** 2
```

## 6 Test Fixtures
