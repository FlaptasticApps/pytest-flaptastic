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

## CircleCI 2.0 Configuration
A simple project might have a CircleCI 2.0 YML that ultimately does a 'make test' like this:
```
      - run: make test
```
In CircleCI 2.0, we must map some of Circle's variables to Flaptastic varibles and include the Flaptastic organization id like this:
```
      - run:
          name: Run PyTest With Flaptastic
          environment:
            FLAPTASTIC_ORGANIZATION_ID: "<your org id goes here>"
            FLAPTASTIC_VERBOSITY: 1
          command: |
            echo 'export FLAPTASTIC_BRANCH=$CIRCLE_BRANCH' >> $BASH_ENV
            echo 'export FLAPTASTIC_LINK=$CIRCLE_BUILD_URL' >> $BASH_ENV
            echo 'export FLAPTASTIC_SERVICE=$CIRCLE_PROJECT_REPONAME' >> $BASH_ENV
            echo 'export FLAPTASTIC_COMMIT_ID=$CIRCLE_SHA1' >> $BASH_ENV
            source $BASH_ENV
            make test
```
Please be sure to pass your selected organization ID as the actual ID value from your Flaptastic account as a string with double quotes. At the time of this writing, CircleCI will botch our 64-bit integer ids without the double quotes.

Finally, find your Flaptastic API token and then go to your CircleCI project page. Navigate to the project environment variables screen and create an enviornment variable called "FLAPTASTIC_API_TOKEN" and then paste your token as the value.

![alt text](https://s3.amazonaws.com/www.flaptastic.com/images/circle.png "Screenshot of how to register the secret token value in CircleCI")


## License

pytest-flaptastic is available under the MIT License.
