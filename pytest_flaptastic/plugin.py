from __future__ import print_function
import requests
import time
import sys
import os
import collections
import re

"""
A pytest plugin for Flaptastic.
"""

queue = collections.deque()
page_size = 3
num_results_sent = 0
param_map = {
    'flaptastic_organization_id': '--flaptastic-organization-id',
    'flaptastic_api_token': '--flaptastic-api-token',
    'flaptastic_commit_id': '--flaptastic-commit-id',
    'flaptastic_branch': '--flaptastic-branch',
    'flaptastic_service': '--flaptastic-service',
    'flaptastic_link': '--flaptastic-link',
    'flaptastic_verbosity': '--flaptastic-verbosity'
}


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
                     action='store', type=str, dest='flaptastic_verbosity',
                     default=os.getenv('FLAPTASTIC_VERBOSITY', '1'), help='Stdout verbosity. 0=none 1=minimal 2=everything')


def missing_options_detected(args_namespace):
    return bool(get_missing_params(args_namespace))


def get_missing_params(args_namespace):
    required_options = [
        'flaptastic_organization_id',
        'flaptastic_api_token',
        'flaptastic_branch',
        'flaptastic_service'
    ]
    missing = []
    for option_name in required_options:
        if not get_option(args_namespace, option_name):
            missing.append("{} ({})".format(
                param_map[option_name],
                option_to_env_name(option_name)
            ))
    return missing


def get_option(args_namespace, option_name):
    """
    Get an option from either the CLI or the environment.
    """
    result = args_namespace.__dict__.get(option_name)
    if not result:
        result = os.getenv(option_to_env_name(option_name))
    return result


def option_to_env_name(option_name):
    return re.sub('[^a-z]', '_', option_name).upper()


def pytest_cmdline_main(config):
    missing = get_missing_params(config.option)
    if missing:
        if int(get_option(config.option, "flaptastic_verbosity")) > 0:
            eprint("Flaptastic plugin will not send test results. "
                   "Missing params: {} https://www.flaptastic.com/documentation".format(missing))


def pytest_terminal_summary(terminalreporter, exitstatus=None):
    if not missing_options_detected(terminalreporter.config.option):
        occasionally_deliver(terminalreporter.config.option, True)
        if int(get_option(terminalreporter.config.option, "flaptastic_verbosity")) > 1:
            eprint("\n{} test results sent to Flaptastic in total.".format(num_results_sent))


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
    global num_results_sent
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
            num_results_sent = num_results_sent + len(test_results)
            if int(get_option(namespace_args, "flaptastic_verbosity")) > 2:
                eprint("{} test results sent to Flaptastic".format(
                    len(test_results)
                ))
        else:
            if int(get_option(namespace_args, "flaptastic_verbosity")) > 0:
                eprint("Failure to deliver test results to Flaptastic: {} - {}".format(
                    r.status_code,
                    r.content.decode()
                ))
