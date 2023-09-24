## 1 - intro to tests

### Why write tests?

might be following some software development methodology that demands it; such as Test Driven Development (TDD).

We want to protect a production branch from bugs and changes that may break the software.

So, we write tests, put them in a test suite, and any time someone wants to make changes to the code, they must first run this test suite (and make sure all the tests are still passing). Very important for large and complex software where something may not be caught at manual inspection points such as code review, or via functional/usability quality assurance testing.

### Why use a test framework?

Dont need to, can write em on our own. but we would be reinventing the wheel (we want to spend more time writing tests and software, not making the functionality to run the tests). Regardless of the software, the desire to parallelize, parameterize, randomize, _, or _ often arises. Some of these features are provided by pytest. But what about the ones that are not? That is the purpose of this report. To extend pytest to cover those edge cases, and provide a written, off the shelf framework that can be used.

## installing pytest

covered in pytest docs (install using pip, see "getting started" page).

```pip install -U pytest```

## next

tests are within python files. these files must be named a certain way. pytest only searches for tests in files with "test" in the name *by default*.

(make a note categorizing the sample tests as unit tests. define unit tests.)
