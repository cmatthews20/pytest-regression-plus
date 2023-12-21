## 1 - intro to tests

```pytest --help```

will want to have second test (cube) to demonstrate test selection more thoroughly.

### Why write tests?

might be following some software development methodology that demands it; such as Test Driven Development (TDD).

We want to protect a production branch from bugs and changes that may break the software.

So, we write tests, put them in a test suite, and any time someone wants to make changes to the code, they must first run this test suite (and make sure all the tests are still passing). Very important for large and complex software where something may not be caught at manual inspection points such as code review, or via functional/usability quality assurance testing.

### Why use a test framework?

Dont need to, can write em on our own. but we would be reinventing the wheel (we want to spend more time writing tests and software, not making the functionality to run the tests). Regardless of the software, the desire to parallelize, parameterize, randomize, _, or _ often arises. Some of these features are provided by pytest. But what about the ones that are not? That is the purpose of this report. To extend pytest to cover those edge cases, and provide a written, off the shelf framework that can be used.

### installing pytest

covered in pytest docs (install using pip, see "getting started" page).

```pip install -U pytest```

### next

tests are within python files. these files must be named a certain way. pytest only searches for tests in files with "test" in the name *by default*. This is also true for function names. Funcs without "test" in the name, will not be considered as tests by the framework. Funcs that are considered to be tests, are actually just end up being run by the framework.

(make a note categorizing the sample tests as unit tests. define unit tests.)

### round 1, funcs and tests

the tests are using a hardcoded number, calling square, getting the result, and comparing against a reference.

### what constitutes a passed test?

if a test gets to the end with no errors, it is considered a pass. note that a failed assert results in an error, and the test is marked as a failed test. this is not the only failure that can arise. calls to functions or any external resource for example would qualify. 

### how do we run these tests? selecting tests?

run the pytest executable that was installed previously.
```pytest```

call pytest on the command line without any arguments: by default, starts in working dir, and searches recursively in sub dirs to find available tests, and run all of them.

can also provide a dir, file, or specific test for pytest if you dont want to use the working dir.

```pytest ./directory_or_filename```

for specific test:

```pytest test_functions.py::test_square```

substring matching. will deselect all tests that cant match with the string provided after the -k flag. This functionality allows for the implicit categorization of tests by their (function) name.

```pytest -k square``` runs one

```pytest -k test``` runs both

### seeing what tests are available

append "collect only" arg to end of pytest command. it will print the hierarchy of tests it was able to find. they are not executed. just collected.

```pytest --collect-only```

## 2 test classes

previously we were looking at standalone test functions. Standalone tests are prefectly fine - but often it is convenient to group tests together with a function they rely upon and/or related data members. Test classes can also be used simply to group related tests. Therefore, test classes must be considered. A test class would allow us to factor out the 5 from each test function for square and cube. Test classes also must be prefixed with "Test". If the prefix is not there, pytest will not look at the members of the class. Please note that the test classes do not share the exact same space in memory for a shared data member such as `num`. Each test will get its own instance of the data. This is by design. It is not desirable for tests to be interacting with eachother underneath the hood. Tests must remain independent.

test selection works the same with classes as it does with standalone tests.

for specific test:

```pytest test_classes.py::TestClass::test_square_class```

## 3 skipping tests

Sometimes, a developer may want to skip certain tests. Therefore, it would be convenient if this was enabled at the code level. This would remove the need to customize the pytest commands in order to skip tests. Pytest includes several ways to do this.

One way to skip tests, is with the `@pytest.mark.skip` decorator. Pytest must be imported to do this. After collection, at the execution stage, the decorator indicates to pytest that this test should not be run.

When running test_skip.py, we see that the yellow s in the command line indicates it has been skipped as intended.

Just as this marker can be added to standalone test functions, it can be added to other test structures, such as test classes. The marker can also be applied to test functions within a class to skip certain functions within a class, while allowing the other test functions within the class to run. To avoid redundant code, this will not be demonstrated with classes. The simplest use cases will be demonstrated in order to reduce complexity while moving towards the solution.

Instead of skipping a test prior to execution, there may be cases where tests should be skipped during execution. I.e. a codepath that isnt implemented is reached; instead of failing the test, or issuing a pseudo-pass, it can be skipped by calling/envoking `pytest.skip()`. This will skip the test and mark it accordingly during execution. This differs from the previous method in code as well, since the skip is taking place within the test body, not just as a function/class decorator.

When a test is skipped, it is important to document why a particular test was skipped. This will ensure any developers (including the author) does not return to the codebase wondering why certain tests were skipped. This can be accomplished by passing a `reason` parameter to the skip decorator as seen below:

`@pytest.mark.skip(reason="skipped test because...")`

By default, this reason is now shown in the output when the tests are run. You can specifiy an increased verbosity in the command line by adding the `-rs` flag (s indicating extra info for skipped tests). Passing this flag will print the skip reason when invoking tests.

Unconditionally skipping tests is not sufficient. Utilizing a slightly different decorator grants the possibility of conditionally skipping tests.

```
import sys
import pytest
@pytest.mark.skipif(sys.version_info > (3,6), reason="Test required python version <= 3.6")
...
```

The skipif decorator will skip the test if the condition passed evaluates to TRUE. A reason is required for skipif decorators. This is just good practice regardless. 

Tests in a certain file can also be skipped based on the success of a package import. Please see the pytest documentation for more information. This method is not covered, as it does not assist the purpose of the report and is outside of the scope. It does assist overall code quality/robustness, but does not assist the devlopment of parallelized regression tests (for scope we can say that only the relevant features of pytest will be covered to avoid overcomplication, restating the documentation, or involving irrelevant material).

## 4 xfail tests

How to deal with tests that cannot succeed? There may be tests that fail that we still want to execute. I.e. when testing a specific failure codepath (want to make sure the code is doing the correct thing, even in the case of a failure)

***skipped***

## 5 parameterizing tests
