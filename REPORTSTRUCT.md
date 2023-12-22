
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

It takes roughly two years and several billion dollars for semiconductor companies to tape-out a new chip. It is important for these companies to thoroughly test and validate their designs. Tools for physical modelling and simulation already exist, such as MATLAB, Ansys, Autodesk, among others. However, the need to extend beyond physical simulation is present. As it stands, these companies need to wait two years for their designs to be implemented, and only then be able to test the algorithms on them. This poses two problems. First; the algorithms the hardware was written for have never been tested on the chip before fabrication. There is no guarantee, through analysis alone, that the algorithms the hardware was designed for will run efficiently. Secondly, with some algorithms, such as artificial intelligence, evolving by the month, semiconductor companies need to inform their designs with perfomance feedback in much shorter intervals than two years. 

It might be easy to assert that these companies should write some software to mathematically calculate the power and performance of the algorithms on current hardware. From there, they could alter the design, or the algorithm to achieve the desired output. They key issue is that hardware testing and software testing is very different. Since hardware could be used for an infinite number of use cases, it is impossible to test every single input. Especially considering analog values for certain inputs, where there are an infinite number of inputs, even between 1V and 2V. To mitigate this, hardware teams will run a massive test suite, with randomized inputs, on their designs. The hope, is that within a two year span, the tests have provided sufficient coverage through randomization. Software algorithm testing, however, is normally 'directed'. There is an exact expected output for every input. Most units of software do not have nearly as many possible expected outputs as a hardware component. As a result, developers only need to test certain cases. Then, by further extension, the frameworks that the software developers have been provided, do not provide the features a hardware engineer would be accustomed to. 

This is the issue this report is aiming to solve. Hardware engineers need to write software, from scratch, to simulate their designs, so they can test the efficacy of the algorithms on their hardware. However, they do not have the testing frameworks needed to test software like they would test hardware. A framework that these hardware engineers could use, at minimum, would require randomization support. Additionally, due to the number of tests a hardware engineer is running, compared to a software engineer, the hardware engineer requires their suites to run much faster. To tackle this issue, this report investigates the feasibility of running tests in parallel, instead of sequentially. This paper hypothesizes that it is possible to create a software wrapper around several pre-existing software testing frameworks, to make it possible to test hardware algorithm simulation software with randomization and parallelization support.

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
