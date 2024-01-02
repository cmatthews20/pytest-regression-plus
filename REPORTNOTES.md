---
output:
  pdf_document
fontsize: 12pt
font: timesnewroman
geometry: "left=2.54cm,right=2.54cm,top=2.54cm,bottom=2.54cm"
---


# Executive Summary

# 1 - Introduction

It takes roughly two years and several billion dollars for semiconductor companies to design and fabricate a new computer chip []. It is important for these companies to thoroughly test and validate their designs. Tools for physical modelling and simulation already exist, such as MATLAB, Ansys, Autodesk, among others []. However, the need to extend beyond physical simulation is present. As it stands, these companies need to wait two years for their designs to be implemented, and only then are they able to test the algorithms on them. This poses two problems. First; the algorithms the hardware was written for will have never been tested on the chip before fabrication. There is no guarantee, through analysis alone, that the algorithms the hardware was designed for will run efficiently. Secondly, with some algorithms, such as artificial intelligence, evolving by the month, semiconductor companies need to inform their designs with perfomance feedback in much shorter intervals. 

It might be easy to assert that these companies should write some software to mathematically calculate the power and performance of the algorithms on current hardware. From there, they could alter the design, or the algorithm to achieve the desired output. They key issue is that hardware testing and software testing is very different. Since hardware could be used for a theoretically infinite number of use cases, it is impossible to test every single input. To mitigate this, hardware teams will run a massive test suite, with randomized inputs, on their designs []. The hope, is that within two years, the tests have provided sufficient coverage through randomization. Software algorithm testing, however, is normally 'directed'. There is an exact expected output for every input. Most units of software do not have nearly as many possible expected outputs as a hardware component. As a result, developers only need to test certain cases. Then, by further extension, the frameworks that the software developers have been provided, do not provide the features a hardware engineer would be accustomed to []. 

This is the issue this report is aiming to solve. Hardware engineers need to write software, from scratch, to simulate their designs, so they can test the efficacy of the algorithms on their hardware. However, they do not have the testing frameworks needed to test software like they would test hardware []. A framework that these hardware engineers could use, at minimum, would require randomization support. Additionally, due to the number of tests a hardware engineer is running, compared to a software engineer, the hardware engineer requires their suites to run much faster. To tackle this issue, this report investigates the feasibility of running tests in parallel, instead of sequentially. This paper hypothesizes that it is possible to create a software wrapper around several pre-existing software testing frameworks, to make it possible to test hardware algorithm simulation software with randomization and parallelization features.


## 1.1 - Purpose

The purpose of this report is multifaceted. First, pytest, a Python testing framework, is investigated to determine its suitability for testing hardware simulation software. In doing so, an extension of pytest is created, to assess its suitability during implementation. Furthermore, this report aims to justify the need for running tests in parallel and then provides experimental data from automated tests run in the cloud.

## 1.2 - Scope

The tools investigated in this report have many features. This report does not comprehensively cover those features; only those necessary to create hardware regression suites are explained and mentioned. Only the relevant features of pytest will be covered to avoid overcomplication, restating the documentation, or involving irrelevant material. Although a light introduction to `pytest` is provided, this report assumes the reader has a preliminary understanding of Python (or an equivalent language for reading purposes), modern coding practices, and software testing. By extension, this report also assumes the reader has a basic understanding of command line interfaces, CI/CD (Continuous Integration/Continuous Delivery) workflows, and how to use a terminal/console/shell. The report often refers to software testing alternatives. For the purpose of this report, the scope of these alternatives is limited to PyUnit, Nose2, Robot, Testify, DocTest, and Robot [].

<div style="page-break-after: always;"></div>
<br />

# 2 - Software Testing

## 2.1 - Why Write Tests?

Writing software tests is a crucial aspect of the software development process. Tests help catch and identify bugs and issues early in the development process. This makes it easier and more cost-effective to fix problems before they become more complex. Writing tests encourages the developer to write modular, maintainable, and loosely coupled code. This, in turn, leads to higher overall code quality. Tests provide a safety net when making changes or adding new features. Having a comprehensive test suite gives developers confidence that their changes won't introduce unexpected issues. With a solid set of tests, developers can refactor code with greater confidence. They can make changes to the codebase, knowing that if something breaks, the tests will catch it. Tests also serve as living documentation for the codebase. They describe how different parts of the code should behave. This can be especially valuable when onboarding new team members or revisiting code after some time. Automated tests can be rerun quickly and easily, allowing you to perform regression testing whenever changes are made. This helps ensure that existing functionality remains intact after modifications. Knowing that a product has a robust set of tests can instill confidence in both development teams and end-users. As requirements change or new features are added, tests act as a safety net, ensuring that existing functionality is not inadvertently broken [].

In summary, writing software tests is an investment in the quality and reliability of the software, with benefits at the code, and business level. It leads to more robust, maintainable code and provides numerous benefits throughout the development life cycle. Additionally, the organization may be following some software development methodology that demands tests from the outset; such as Test Driven Development (TDD) [].

After correctly asserting that tests are required - tests are written, and placed in a test suite, and any time someone wants to make changes to the code, they must first run this test suite (and make sure all the tests are still passing). This is very important for large and complex software where something may not be caught at manual inspection points such as code review, or through quality assurance testing.

## 2.2 - Test Frameworks

Test frameworks enable a developer to design, implement, and execute tests. These frameworks typically provide additional features, such as test case structures, test runners, test reporting, and setup/teardown mechanisms []. A developer does not need to use a testing framework; they can certainly write their own. However, they would be 'reinventing the wheel', since a way to run the tests needs to be created. Developers want to spend more time writing tests and software, not making the functionality to run the tests. Regardless of the software, the desire to parallelize, parameterize, or randomize often arises. Some of these features are provided by `pytest`. The purpose of this section To extend `pytest` to create the features that are not provided, and yield a written, off-the-shelf framework that can be used.

<div style="page-break-after: always;"></div>

# 3 - Creating the Framework Wrapper

## 3.1 - Installing pytest

Install pytest by entering the following into the terminal shell [].

```bash
pip install -U pytest

# run to ensure successful install
pytest --help
```

## 3.2 - Basics

In `pytest`, tests are within Python files. These files must be named a certain way. By default, `pytest` only searches for tests in files with `test` in the name. This is also true for function names. Funcions without `test` in the name, will not be considered as tests by the framework. Functions that are considered to be tests are run by the framework. A sample function and accompnaying test can be seen below. The test is run using a hardcoded number, calling the function, getting the result, and comparing against a reference.

```python
def square(num):
    """
    Simple function that squares a number.
    """

    return num * num

def test_square():
    """
    Unit test for square function
    """
    num = 5
    result = square(num)
    assert result == num ** 2

```

If a test gets to the end with no errors, it is considered a pass. A failed assert statement results in an error, and the test is marked as a failed test. This is not the only failure that can arise [].

## 3.3 - Running and Selecting Tests

To run the tests/suite, run the `pytest` executable. Calling `pytest` on the command line without any arguments - by default, starts in working dir, and searches recursively in sub-directories to find available tests, and runs all of them. The executable can be run with the `-s` flag since `pytest` wants to hide a lot of output to keep things clean. A directory, file, or specific test can also be provided to the executable

```bash
# Run all tests
pytest

# run tests in given directory
pytest ./directory_or_filename

# run a specific test
pytest test_functions.py::test_square
```

See below an example of substring matching. This method will deselect all tests that do not match with the string provided after the `-k` flag. This functionality allows for the implicit categorization of tests by their (function) name.

```bash
# runs one
pytest -k square
``` 

```bash
# runs both
pytest -k test
``` 

## 3.4 Collecting Tests

Collecting tests is a method that allows the developer to visualize what tests are available. Appending the `--collect-only` flag to end of `pytest` command prints (lists) the hierarchy of tests that are available. These tests are not executed; they are collected and shown to the developer.

```bash
pytest --collect-only
```

## 3.5 - Test Classes

Previous sections discussed standalone test functions. Standalone tests are prefectly fine - but often it is convenient to group tests together with a function they rely upon and/or related data members. Test classes can also be used to group related tests. Therefore, test classes must be considered. Building on the previous example, a test class would allow the factoring out the `num` variable from the test function. Test classes also must be prefixed with `Test`. If the prefix is not there, `pytest` will not look at the members of the class. Note that the test classes do not share the exact same space in memory for a shared data member such as `num`. Each test will get its own instance of the data. This is by design. It is not desirable for tests to be interacting with eachother. Tests must remain independent.

```python
class TestClass:
    # Share this common number between test instances
    num = 5

    def test_square_class(self):
        result = square(self.num)
        assert result == self.num ** 2
```

 Test selection works the same with classes as it does with standalone tests, as seen below.

```bash
pytest test_classes.py::TestClass::test_square_class
```

## 3.6 - Skipping Tests

Sometimes, a developer may want to skip certain tests. Therefore, it would be convenient if this was enabled at the code level. This would remove the need to customize the `pytest` commands in order to skip tests. `pytest` includes several ways to do this. One way to skip tests, is with the `@pytest.mark.skip` decorator. `pytest` must be imported to do this. After collection, at the execution stage, the decorator indicates to pytest that this test should not be run.

Just as this marker can be added to standalone test functions, it can be added to other test structures, such as test classes. The marker can also be applied to test functions within a class to skip certain functions within a class, while allowing the other test functions within the class to run. To avoid redundant code, this will not be demonstrated in the report. The simplest use cases will be demonstrated in order to reduce complexity while moving towards the solution.

Instead of skipping a test prior to execution, there may be cases where tests should be skipped during execution. For example, a codepath that is not implemented is reached; instead of failing the test, or issuing a pseudo-pass, it can be skipped by calling `pytest.skip()`. This will skip the test and mark it accordingly during execution. This differs from the previous method in code as well, since the skip is taking place within the test body, not just as a function/class decorator.

When a test is skipped, it is important to document why a particular test was skipped. This will ensure any developers (including the author) does not return to the codebase wondering why certain tests were skipped. This can be accomplished by passing a `reason` parameter to the skip decorator as seen below:

```python
@pytest.mark.skip(reason="skipped test because...")
```

By default, this reason is now shown in the output when the tests are run. Increased verbosity can be specified in the command line by adding the `-rs` flag. Passing this flag will print the skip reason when invoking tests. Unconditionally skipping tests is not sufficient. Utilizing a slightly different decorator grants the possibility of conditionally skipping tests. The `skipif` decorator will skip the test if the condition passed evaluates to `TRUE`. A reason is required for `skipif` decorators.

```python
import sys
import pytest
@pytest.mark.skipif(sys.version_info > (3,6), reason="Test required python version <= 3.6")
# ...
```

Tests in a certain file can also be skipped based on the success of a package import. Please see the `pytest` documentation for more information. This method is not covered, as it does not assist the purpose of the report and is outside of the scope. It does assist overall code quality/robustness but does not assist the development of parallelized regression tests.

## 3.7 - Parameterizing Tests

This section will introduce the concept of test parameterization in pytest. In previous sections, basic examples have been used. These tests are referred to as directed tests, because the test inputs were hardcoded into the tests themselves. In directed tests, a hardcoded input is given which should always yield the same output. While this is perfectly suitable for simple tests or functions that are only designed for a single input, often times a developer will need to vary the inputs. Pytest provides this functionality with another decorator. The test seen below will test the square function three times, using numbers one through three for each input.

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

This marks the starting point for incorporating randomized tests into the framework wrapper. Although it would be easy to tell the developer to write randomized tests as seen below, it would not provide any additional value. The aim is to provide a framework for doing so without introducing any hardcoded randomized values while factoring out and centralizing this functionality. This method also has issues when tests are distributed among different CPU's for parallelization. Randomizing at the function level does not work for parallel tests. Parallel tests will throw errors if a different random value is generated by different CPU's. So, the wrapper must find a way to broadcast a consistent random value in a single session.

```python
import random

# this causes problems in parallel pipeline
@pytest.mark.parametrize("num", [random.randint(1, 10)])
def test_square_param(num):
    result = square(num)
    assert result == num ** 2
```

Pytest also allows the parametrization of tests where values are independent of one another. In the following case, the inputs are varied independently, essentially computing the cartesian product of the `base` and `exponent` lists, creating all possible combinations as inputs to the test. Although this will not be used further to avoid any over-complication of the explanation of the framework wrapper, it will be used when testing real software.

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


## 3.8 - Test Fixtures

It is often the case that developers want to perform some initialization of their test functions. This initialization should not take place in the body of the tests. This avoids cluttering the test bodies and avoids repeated code in the case that the same initialization should take place in several tests. To address the broadcasting issue, we must write a fixture. A fixture with a session-wide scope will enable us to broadcast the same random value to each test, allowing the parallelization to take place. The `autouse=True` flag within the fixture decorator has been purposely avoided. We want to broadcase the same value. Autouse would cause the fixture to run at the beginning of each run, which would pose the same issue with the built-in parametrize decorator. However, this flag would be very useful for logging at the beginning of each test.

```python
@pytest.fixture(scope="session")
def rand_val():
    rand_int = random.randint(1, 10)
    return rand_int

def test_square_param(rand_val):
    print(rand_val)
    result = square(rand_val)
    assert result == rand_val ** 2
```

Running the following on the command line will enable the developer to see what fixures are available to them. This command should be known by developers who use this wrapper - in the next session, fixtures will be provided implicitly.

```bash
pytest --fixtures [pathname]
```

## 3.9 - Test Configurations

This section covers the creation of a `conftest.py` file to complete the wrapper. Developers using this framework wrapper will want to use the fixture throughout their suites. It does not make sense to repeat code for tests in different files that want to use the same fixture. This is where the test configuration file comes in. This file should be created so no refactors are needed when tests are written (no import needed so test files do not need to be modified). This file style can be duplicated in different directories. pytest can decipher which to use based on the location of the file relative to the tests (tests will use the conftest within their directory). This is useful when a developer wants to overload a function without having to be worried about orchestrating the use of the correct function where it is called.

```python
# conftest.py

@pytest.fixture(scope="session")
def rand_val_10():
    rand_int = random.randint(1, 10)
    return rand_int

@pytest.fixture(scope="session")
def rand_val_20():
    rand_int = random.randint(1, 20)
    return rand_int

# ...
```

## 3.10 - Adding Command Line Options

Using initialization hooks, command line options can be added. This is a crucial feature of the framework wrapper, as it is the mechanism that provides additional functionality to the developer. Options allow the developer to control certain values of a test from the command line. This is mostly for convenience. If a developer needs to change a certain part of a test, instead of opening the file and changing the source code, they can pass a value to the command line option. An `argparse` style option will be added to the pytest parser. Running `pytest --help` will enable the developer to see the options the wrapper has added. See the example below.

```python
# in the conftest file
def pytest_addoption(parser):
    parser.addoption("--example", action="store", default="example string")

@pytest.fixture
def name(request):
    return request.config.getoption("--example")

# in the test file

def example_test(example):
    assert example = "pass"

```

## 3.11 - Dynamic Parameters

This section will discuss dynamic parametrization. A developer may want to change how a test is parametrized at runtime or adjust the variants that exist. For this report, the number of variants needs to be adjusted. As per the previous section, this will be controlled with a command line argument.

Previously, tests were parametrized using a decorator. However, at this stage, it is clear that parametrization cannot be static. It must be done dynamically. This will be accomplished with another hook, `pytest_generate_tests`. This hook should be located in the conftest file, with the other fixtures. The `pytest_generate_tests` contains a `metafunc` object. This object can be leveraged to perform the dynamic parametrization since it allows aspects of the tests to be accessed in the `conftest` file at runtime. This enables the creation of code that alters the tests after they are written - a crucial paradigm that does not exist in the currently available framework alternatives. In the hook, a check ensures the fixture is present in the test. It ensures the value being parametrized is being requested by the test. If the fixture is present in the test, parametrization can then take place. Run `pytest --collectonly test_dynamic_param.py` to see the variants produced.

```python

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
```

Adding a file option would further bridge the hardware-software testing gap, as hardware tests usually pull from a file of manual tests []. These files have inputs and desired outputs and can be used to assess whether or not a system has regressed. A seeding option is added as well. This will ensure the workers have consistently broadcasted tests. This enables the framework to work around a known limitation of `xdist`, as well as enabling specific test repeats.

## 3.12 - Parallelism via the `xdist` Plugin

This section investigates parallelizing tests with the `xdist` plugin. `xdist` provides alternate test execution modes. Using this plugin, the framework wrapper can instruct pytest to spawn several worker processes. These worker processes can only be spawned if there is a CPU available, and the number of workers cannot exceed the number of available CPUs. Tests can be randomly distributed across available CPUs and run concurrently as seen below [].

```bash
# Spawn the maximum number of workers permitted
pytest -n auto 

# Spawn 2 workers
pytest -n 2
```

Running traditional software tests serially is sometimes acceptable. These suites rarely exceed ten minutes []. However, most nightly hardware random regression suites can take upwards of two hours []. A method to reduce test time must be explored. One such way, is through parallelization (concurrent execution).

There are some issues to consider with parallelization. Overparallelization, for example, is possible, since each worker process is competing for the resources on the same machine. If over-parallelization occurs, out-of-memory errors, for example, can occur. How many workers to use is normally evaluated on a case-by-case basis. However, an experiment can be constructed to find the optimal number of workers.

## 3.13 - Setup File

Previously, the pytest runner was configured in the command line. Remembering all these options can be cumbersome. The command line options can also be configured within the `setup.cfg` file. Some common use cases include selecting command line options to be used by default, adding new markers, and adding to the test discovery regular expression options. This would allow categorization with the following command `pytest -m custom_marker`, which would run all tests with certain markers. There are many other configuration options available [].

<div style="page-break-after: always;"></div>

# 4 - Experiment

## 4.1 - Setup

For this framework wrapper to be viable, the tests must be able to be randomizable while running in parallel. This must also be able to take place in the cloud. For a software system to be complete, it must have a Continuous Integration and Continuous Delivery (CI/CD) workflow/pipeline. This pipeline runs on the code repository, which is stored online [].

This experiment aims to prove that random tests can be run in parallel, that running them in parallel saves time, and that parallel randomized tests can be run in the cloud. To do so, the following `.yml` file was created. This file instructs GitHub Actions on how to set up the test environment and run the tests. GitHub Actions is a CI/CD platform that allows the build, test, and deployment pipeline to be automated []. For this experiment, only the build and test features are utilized.

```yml
name: Cloud Automated Tests

on: 
  push:
    branches: [main]

jobs:
  workflow:
    runs-on: ubuntu-latest
    permissions: write-all
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3
  
      - name: Set up Python ${{ matrix.python-version }}  
        uses: actions/setup-python@v4  
        with:  
          python-version: ${{ matrix.python-version }}  
      - name: Install dependencies  
        run: |  
          python -m pip install --upgrade pip
          python -m pip install pytest
          pip install pytest-xdist
          pip install numpy

      - name: Run Tests
        run: |
          cd src
          python -m pytest test_dynamic_param.py --num_seeds=?

      - name: Run Tests in Parallel
        run: |
          cd src
          python -m pytest test_dynamic_param.py --num_seeds=? -n ?

```

Most hardware tests are seeded so that they can be repeated in the case of failure. Seeding refers to keeping track of the state of the randomizer object so that certain runs can be replicated by feeding the randomizer the same seed. Therefore, a seeding option is necessary for hardware developers to use the framework wrapper. Additionally, due to `xdist` limitations, the same seed must be broadcasted to each CPU. If each CPU generates different test variants to select from, an error occurs. As seen below, a command line option for the test seed must be added. To give the developer a way to amend the number of random tests to run, and to facilitate this experiment, a `num_seeds` option is also added. This will dictate how many random test variants are generated. See below the resulting python files. 

```python
# conftest.py
import pytest
import numpy as np

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

# test_dynamic_param.py

from functions import square
import time

def test_square_dynamic(rand_val):
    result = square(rand_val)
    print(rand_val)
    time.sleep(1)
    assert result == rand_val ** 2
```

Before analyzing the data, it is important to note that setting up a worker process consumes a non-negligible, variable amount of time. It is assumed that the optimal number of workers depends on the number of tests being run and the length of each test. This experiment is run across the three latest Python versions, each with sequential run control groups. 

## 4.2 - Results

See Appendix A for the entire experiment dataset or Appendix B for tabularized results from each run. At first approach to the problem, one could lazily assume that the optimal number of workers is as many as possible. The most obvious problem with this is that spawning a worker consumes time. If x is the number of tests being run, spawning any amount of workers greater than x wastes time. Workers are unable to run a fraction of a test, which would leave certain workers without any test to run. This puts the theoretical limit at x amount of workers for x number of tests. A single worker is also not a viable option. This would result in no parallel tests and would result in more time elapsing than a normal run in series due to the setup time. However, if the tests are not sufficiently large in duration or number, the worker setup time is not worth the cost. The experiment assumes the test lengths and amounts are non-trivial. This is a safe assumption to make given the target audience of this framework wrapper has large test suites with long individual test times. From these assumptions and analyses, the sample space is limited to the following.

```
2 < optimal number of workers <= x, where x = number of tests
```

The results support this analysis. Spawning more workers than tests occasionally results in an overall decrease in runtime when compared to series runs, but this is never the optimal case. The results also uncovered an interesting phenomena with respect to local optima. If the number of workers is less than the number of tests, various local optima appear. This is due to the relationship between the number of tests, and its divisibility with respect to the number of workers. If spawning another worker does not decrease the number of tests held by the worker with the most tests, it performs worse than the nearest number of workers which can divide the number of tests evenly. This effect exacerbates itself as test length and amount decrease, and is most pronounced around the square root of the number of tests. Taking a deeper dive into the data, if worker setup time is much less than the average individual test run time and the amount of tests is non-trivial, then the optimal number of workers is equal to the number of tests.

<div style="page-break-after: always;"></div>

# 5 - Conclusion

`pytest` was determined to be a suitable candidate for running hardware-based tests in software. A framework wrapper was successfully created to facilitate these tests, with randomization and parallelization features. An experiment determined the optimal number of worker processes for parallel test runs and asserted the possibility of parallel tests in the cloud.

## 5.1 - Recommendations

To optimize the usability and adoption of the framework wrapper created herein, the inclusion of additional quality-of-life features that cater to the needs and expectations of testing engineers should be considered. Features such as enhanced test reporting, built-in mocking, an extended assertion library, and automated management of dynamic test data should be investigated.

To promote accessibility and ease of integration, the framework should be installable via the Python Package Index (PyPI) using the pip package manager. Creating and uploading a package distribution on PyPI would simplify the installation process for end-users and ensure adherence to best practices for versioning and dependency management to ensure compatibility with various Python environments.

Developers who parallelize their tests should also profile them. Using the `--durations` flag, they can see their longest tests and optimize as needed.

Additionally, traditional software documentation for this framework wrapper should be written. This style of reporting is not commonplace for software packages, which may inhibit its adoption. As such, it should be re-styled and placed on a website with an accompanying tutorial.

By incorporating these recommendations, the testing framework will meet the expectations of testing engineers and have the potential to become a valuable asset within the software development community. The availability of the framework on PyPI will further contribute to its accessibility, enabling engineers to integrate it into their projects.

<div style="page-break-after: always;"></div>

# Appendix A - Code Repository and CI/CD Pipeline

Code Repository - https://github.com/cmatthews20/pytest-regression-plus 

CI/CD Pipeline (Experiment Results) - https://github.com/cmatthews20/pytest-regression-plus/actions 

<div style="page-break-after: always;"></div>

# Appendix B - Tabulated Results

Key: Time (Parallel) / Time (Sequential)

Test Length = 1s

|Python Version|No. Tests | No. Workers | Time (s) |
|--:|---|---|---|
|3.10 | 25 | 2 |13.50 / 25.09|
|3.10 | 25 | 3 |9.68|
|3.10 | 25 | 4 |7.87|
|3.10 | 25 | 5 |6.10|
|3.10 | 25 | 6 |6.27|
|3.10 | 25 | 7 |5.45|
|3.10 | 25 | 8 |5.70|
|3.11 | 25 | 2 |13.57 / 25.06|
|3.11 | 25 | 3 |9.80|
|3.11 | 25 | 4 |8.00|
|3.11 | 25 | 5 |6.22|
|3.11 | 25 | 6 |6.42|
|3.11 | 25 | 7 |5.68|
|3.11 | 25 | 8 |5.89|
|3.12 | 25 | 2 |13.50 / 25.05|
|3.12 | 25 | 3 |9.68|
|3.12 | 25 | 4 |7.87|
|3.12 | 25 | 5 |6.11|
|3.12 | 25 | 6 |6.33|
|3.12 | 25 | 7 |5.51|
|3.12 | 25 | 8 |5.70|
|3.10 | 100 | 2 |50.69 / 100.33|
|3.10 | 100 | 3 |34.78|
|3.10 | 100 | 4 |25.94|
|3.10 | 100 | 5 |21.20|
|3.10 | 100 | 6 |18.36|
|3.10 | 100 | 7 |16.56|
|3.10 | 100 | 8 |14.79|
|3.11 | 100 | 2 |50.56 / 100.19|
|3.11 | 100 | 3 |34.70|
|3.11 | 100 | 4 |25.84|
|3.11 | 100 | 5 |21.02|
|3.11 | 100 | 6 |18.17|
|3.11 | 100 | 7 |16.36|
|3.11 | 100 | 8 |14.55|
|3.12 | 100 | 2 |50.72 / 100.21|
|3.12 | 100 | 3 |34.81|
|3.12 | 100 | 4 |26.01|
|3.12 | 100 | 5 |21.20|
|3.12 | 100 | 6 |18.40|
|3.12 | 100 | 7 |16.58|
|3.12 | 100 | 8 |14.83|


Test Length = 5s

|Python Version|No. Tests | No. Workers | Time (s) |
|--:|---|---|---|
|3.10 | 25 | 2 |50.56 / 100.19|
|3.10 | 25 | 4 |25.84|
|3.10 | 25 | 8 |16.61|
|3.10 | 25 | 10|11.97|
|3.10 | 25 | 12|12.43|
|3.11 | 25 | 2 |50.55 / 100.06|
|3.11 | 25 | 4 |25.92|
|3.11 | 25 | 8 |16.77|
|3.11 | 25 | 10|12.32|
|3.11 | 25 | 12|12.70|
|3.12 | 25 | 2 |50.67 / 100.09|
|3.12 | 25 | 4 |26.13|
|3.12 | 25 | 8 |17.11|
|3.12 | 25 | 10|12.55|
|3.12 | 25 | 12|13.08|
|3.10 | 10 | 2 |25.50 / 50.08|
|3.10 | 10 | 4 |15.87|
|3.10 | 10 | 8 |11.62|
|3.10 | 10 | 10|6.95|
|3.10 | 10 | 15|7.93|
|3.10 | 10 | 20|8.86|
|3.11 | 10 | 2 |25.45 / 50.03|
|3.11 | 10 | 4 |15.79|
|3.11 | 10 | 8 |11.49|
|3.11 | 10 | 10|6.85|
|3.11 | 10 | 15|7.85|
|3.11 | 10 | 20|8.71|
|3.12 | 10 | 2 |25.66 / 50.05|
|3.12 | 10 | 4 |16.11|
|3.12 | 10 | 8 |12.12|
|3.12 | 10 | 10|7.59|
|3.12 | 10 | 15|8.87|
|3.12 | 10 | 20|10.23|


