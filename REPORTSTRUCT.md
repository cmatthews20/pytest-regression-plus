
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


## Executive Summary

## Purpose

The purpose of this report is multifaceted. First, pytest, a Python testing framework, is investigated to determine its suitability for testing hardware simulation software. In doing so, an extension of pytest is created, to assess its suitability during implementation. Furthermore, this report aims to justify the need for running tests in parallel and then provides experimental data from automated tests run in the cloud.

## Scope

The tools investigated in this report have many features. This report does not comprehensively cover those features; only those necessary to create hardware regression suites are explained and mentioned. Although a light introcuction to pytest is provided, this report assumes the reader has a preliminary understanding of Python (or an equivalent language for reading purposes), modern coding practices, and pure software testing. By extension, this report also assumes the reader has a basic understanding of command line interfaces, CI/CD (Continuous Integration/Continuous Delivery) workflows, and how to use a terminal/console/shell.

## Conclusion

## Recommendations

To optimize the usability and adoption of the framework wrapper created herein, the inclusion of additional quality-of-life features that cater to the needs and expectations of testing engineers should be considered. Features such as enhanced test reporting, built-in mocking, an extended assertion library, and automated management of dynamic test data should be investigated.

To promote accessibility and ease of integration, the framework should be installable via the Python Package Index (PyPI) using the pip package manager. Creating and uploading a package distribution on PyPI would simplify the installation process for end-users and ensure adherence to best practices for versioning and dependency management to ensure compatibility with various Python environments.

Additionally, traditional software documentation for this framework wrapper should be written. This style of reporting is not commonplace for software packages, which may inhibit its adoption. As such, it should be re-styled and placed on a website with an accompanying tutorial.

By incorporating these recommendations, the testing framework will meet the expectations of testing engineers and have the potential to become a valuable asset within the software development community. The availability of the framework on PyPI will further contribute to its accessibility, enabling engineers to integrate it into their projects.
