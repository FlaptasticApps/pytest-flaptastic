# pytest-flaptastic
Py.test plugin for Flaptastic.

https://www.flaptastic.com/

## Installation

To install pytest-flaptastic:

    $ pip install pytest-flaptastic

Environment variables:

| Required | Environment Variable Name  | Description |
| -------- | -------------------------- | ----------- |
| Yes      | FLAPTASTIC_ORGANIZATION_ID | Organization id |
| Yes      | FLAPTASTIC_API_TOKEN       | API token |
| Yes      | FLAPTASTIC_SERVICE         | Name of service (aka microservice) under test |
| No       | FLAPTASTIC_BRANCH          | Branch name being tested. In git, you might pass "master" or names like "myFeature" |
| No       | FLAPTASTIC_COMMIT_ID       | Version id of code tested. In git, this would be the commit sha |
| No       | FLAPTASTIC_LINK            | Link to CI (Jenkins/Circle/Travis etc) website page where you can find the full details of the test run, if applicable |
| No       | FLAPTASTIC_VERBOSITY       | Stdout verbosity. 0=none 1=minimal 2=everything |

Example call pattern:

    $ FLAPTASTIC_ORGANIZATION_ID=123 \
      FLAPTASTIC_API_TOKEN=foo \
      FLAPTASTIC_SERVICE=monolith \
      FLAPTASTIC_BRANCH=master \
      FLAPTASTIC_COMMIT_ID=2feffa9bf0bf3fc48f9f9e89c5386afe0cb77124 \
      FLAPTASTIC_LINK=http://jenkins.example.com \
      py.test
