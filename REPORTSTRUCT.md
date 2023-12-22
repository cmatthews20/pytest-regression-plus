categorization

parameterization

randomization (directed obviously exists)

seeding and repeats

regression?

parallelism

incremental testing

test variants instead of repeated code

Mention requirements and versions used for pytest, xdist, python, pip, time, etc

get the snippet from bob snap

cant test hw <-> sw. make the connection between randomization and the wrapper being created.

Where certain justifications may be vague, please note that I am bound by certain NDA clauses. This report is meant to provide additional value to my employer. as such, the intended audience is an engineer at a similar level as my supervisor (or similar persons).

pytest_collection_modifyitems hook can be used to run based on certain categories. Tests can be skipped based on CLI options or selected/deselected based on enviroment variables.

The pytest cache can be used to store seeds and test results, ensure new test cases are generated with inter-run seed visibility, in addition to skipping initialization steps that have already taken place. (there is evidence to suggest that ...)