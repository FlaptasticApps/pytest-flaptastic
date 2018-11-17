from __future__ import print_function
import requests
import time
import sys
import os
import collections

"""
A pytest plugin for Flaptastic.
"""

queue = collections.deque()
page_size = 3


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def pytest_addoption(parser):
    group = parser.getgroup('flaptastic')
    group._addoption('--flaptastic-organization-id',
                     action='store', type=str, dest='flaptastic_organization_id',
                     default=None, help='Flaptastic organization id')
    group._addoption('--flaptastic-api-token',
                     action='store', type=str, dest='flaptastic_api_token',
                     default=None, help='Flaptastic api token')
    group._addoption('--flaptastic-commit-id',
                     action='store', type=str, dest='flaptastic_commit_id',
                     default=None, help='Source control commit id (git sha)')
    group._addoption('--flaptastic-branch',
                     action='store', type=str, dest='flaptastic_branch',
                     default=None, help='Branch name under test')
    group._addoption('--flaptastic-service',
                     action='store', type=str, dest='flaptastic_service',
                     default=None, help='Identifier for service under test')
    group._addoption('--flaptastic-link',
                     action='store', type=str, dest='flaptastic_link',
                     default=None, help='Optional link to CI page with full details')
    group._addoption('--flaptastic-verbosity',
                     action='store', type=str, dest='verbosity',
                     default='1', help='Stdout verbosity. 0=none 1=minimal 2=everything')


def missing_options_detected(args_namespace):
    return bool(get_missing_params(args_namespace))


def get_missing_params(args_namespace):
    required_options = [
        'flaptastic_organization_id',
        'flaptastic_api_token',
        'flaptastic_commit_id',
        'flaptastic_branch',
        'flaptastic_service',
        'flaptastic_link'
    ]
    missing = []
    for option_name in required_options:
        if not get_option(args_namespace, option_name):
            missing.append(option_name)
    return missing


def get_option(args_namespace, option_name):
    """
    Get an option from either the CLI or the environment.
    """
    return args_namespace.__dict__.get(
        option_name,
        os.getenv(option_name.upper())
    )


def pytest_cmdline_main(config):
    missing = get_missing_params(config.option)
    if not missing:
        if int(get_option(config.option, "flaptastic_verbosity")) > 0:
            eprint("Flaptastic plugin activated.")
    else:
        eprint("Flaptastic plugin is not activated. Missing params: {}".format(
            missing
        ))


def pytest_terminal_summary(terminalreporter, exitstatus=None):
    occasionally_deliver(terminalreporter.config.option, True)


def pytest_runtest_makereport(item, call):
    if not missing_options_detected(item.session.config.known_args_namespace):
        if call.when == 'call':
            send_test_result(item, call)


def send_test_result(item, call):
    test_result = {
      "exception": None if call.excinfo is None else str(call.excinfo.value),
      "file": item.location[0],
      "line": call.excinfo.traceback[len(call.excinfo.traceback)-1].lineno if call.excinfo else item.location[1],
      "name": item.name,
      "status": "failed" if call.excinfo is not None else "success"
    }
    queue.append(test_result)
    occasionally_deliver(item.session.config.known_args_namespace)


def occasionally_deliver(namespace_args, force_dump=False):
    if len(queue) > page_size or force_dump:
        test_results = []
        for i in range(len(queue) if force_dump else page_size):
            test_results.append(queue.popleft())
        doc = {
            "branch": get_option(namespace_args, "flaptastic_branch"),
            "commit_id": get_option(namespace_args, "flaptastic_commit_id"),
            "link": get_option(namespace_args, "flaptastic_link"),
            "organization_id": get_option(namespace_args, "flaptastic_organization_id"),
            "service": get_option(namespace_args, "flaptastic_service"),
            "timestamp": str(int(time.time())),
            "test_results": test_results
        }
        r = requests.post(
            'https://frontend-api.flaptastic.com/api/v1/ingest',
            json=doc,
            headers={
                'Bearer': get_option(namespace_args, "flaptastic_api_token")
            },
            timeout=3
        )
        if r.status_code == 201:
            if int(get_option(namespace_args, "flaptastic_verbosity")) > 1:
                eprint("{} test results sent to Flaptastic".format(
                    len(test_results)
                ))
        else:
            if int(get_option(namespace_args, "flaptastic_verbosity")) > 0:
                eprint("Failure to deliver test results to Flaptastic: {} - {}".format(
                    r.status_code,
                    r.content.decode()
                ))
