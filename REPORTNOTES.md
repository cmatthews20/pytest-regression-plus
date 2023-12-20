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