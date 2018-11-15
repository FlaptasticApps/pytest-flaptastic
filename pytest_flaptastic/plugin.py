"""
A pytest plugin which helps tracking flappy tests.
"""
import socket
import json
import hashlib
import time

# ############### pytest hooks ################


def pytest_addoption(parser):
    group = parser.getgroup('flaptastic')
    group._addoption('--flaptastic-account-id',
                     action='store', type=str, dest='flaptastic_organization_id',
                     default=None, help='Flaptastic organization id')
    group._addoption('--flaptastic-api-token',
                     action='store', type=str, dest='flaptastic_api_token',
                     default=None, help='Flaptastic api token')
    group._addoption('--flaptastic-commit-id',
                     action='store', type=str, dest='commit_id',
                     default=None, help='Source control commit id (git sha)')
    group._addoption('--flaptastic-branch',
                     action='store', type=str, dest='branch',
                     default=None, help='Branch name under test')
    group._addoption('--flaptastic-secret',
                     action='store', type=str, dest='flaptastic_secret',
                     default=None, help='Secret key for flaptastic')
    group._addoption('--flaptastic-service',
                     action='store', type=str, dest='flaptastic_service',
                     default=None, help='Identifier for service under test')
    group._addoption('--flaptastic-link',
                     action='store', type=str, dest='flaptastic_link',
                     default=None, help='Optional link to CI page with full details')


def pytest_runtest_makereport(item, call):
    if call.excinfo is not None:
        if item.session.config.getoption("flaptastic_organization_id"):
            send_flap(item, call)


def send_flap(item, call):
    organization_id = item.session.config.getoption("flaptastic_organization_id")
    api_token = item.session.config.getoption("flaptastic_api_token")
    commit_id = item.session.config.getoption("commit_id")
    branch = item.session.config.getoption("branch")
    flaptastic_secret = item.session.config.getoption("flaptastic_secret")
    flaptastic_service = item.session.config.getoption("flaptastic_service")
    flaptastic_link = item.session.config.getoption("flaptastic_link")
    host = "api.flaptastic.com"
    port = 6789
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = {
        "service": flaptastic_service,
        "commit_id": commit_id,
        "branch": branch,
        "link": flaptastic_link,
        "test_results": {
            "exception": str(call.excinfo.value),
            "file": item.location[0],
            "name": item.name,
            "line": call.excinfo.traceback[len(call.excinfo.traceback)-1].lineno,
        }
    }
    ts = int(time.time())
    document = {
        "organization_id": organization_id,
        "api_token": api_token,
        "timestamp": ts,
        "signature": hashlib.md5(
            "{}-{}-{}".format(
                flaptastic_secret,
                ts,
                json.dumps(payload)
            ).encode()
        ).hexdigest(),
        "payload": payload
    }
    client_sock.sendto(json.dumps(document).encode(), (host, port))
