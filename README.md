# pytest-flaptastic
Py.test plugin for Flaptastic.

https://www.flaptastic.com/

## Installation

To install pytest-flaptastic:

    $ pip install pytest-flaptastic

Then run your tests with either environment variables or switches:

Configuration Options

| Required | Pytest Switch Name           | Environment Variable Name  | Description |
| -------- | ---------------------------- | -------------------------- | ----------- |
| Yes      | --flaptastic-organization-id | FLAPTASTIC_ORGANIZATION_ID | Organization id |
| Yes      | --flaptastic-api-token       | FLAPTASTIC_API_TOKEN       | API token |
| Yes      | --flaptastic-service         | FLAPTASTIC_SERVICE         | Name of service (aka microservice) under test |
| No       | --flaptastic-branch          | FLAPTASTIC_BRANCH          | Branch name being tested. In git, you might pass "master" or names like "myFeature" |
| No       | --flaptastic-commit-id       | FLAPTASTIC_COMMIT_ID       | Version id of code tested. In git, this would be the commit sha |
| No       | --flaptastic-link            | FLAPTASTIC_LINK            | Link to CI (Jenkins/Circle/Travis etc) website page where you can find the full details of the test run, if applicable |
| No       | --flaptastic-verbosity       | FLAPTASTIC_VERBOSITY       | Stdout verbosity. 0=none 1=minimal 2=everything |

Environment variables call pattern style:

    $ FLAPTASTIC_ORGANIZATION_ID=123 \
      FLAPTASTIC_API_TOKEN=foo \
      FLAPTASTIC_SERVICE=monolith \
      FLAPTASTIC_BRANCH=master \
      FLAPTASTIC_COMMIT_ID=2feffa9bf0bf3fc48f9f9e89c5386afe0cb77124 \
      FLAPTASTIC_LINK=http://jenkins.example.com \
      py.test

Switches call pattern style:

    $ py.test \
      --flaptastic-organization-id=123 \
      --flaptastic-api-token=foo \
      --flaptastic-service=monolith \
      --flaptastic-branch=master \
      --flaptastic-commit-id=2feffa9bf0bf3fc48f9f9e89c5386afe0cb77124 \
      --flaptastic-link=http://jenkins.example.com
