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
    group._addoption('--flaptastic-key',
                     action='store', type=str, dest='flaptastic_key',
                     default=None, help='Flaptastic private project secret')
    group._addoption('--commit-id',
                     action='store', type=str, dest='commit_id',
                     default=None, help='Source control commit id (git sha)')
    group._addoption('--branch',
                     action='store', type=str, dest='branch',
                     default=None, help='Branch name under test')
    group._addoption('--flaptastic-secret',
                     action='store', type=str, dest='flaptastic_secret',
                     default=None, help='Secret key for flaptastic')


def pytest_runtest_makereport(item, call):
    if call.excinfo is not None:
        if item.session.config.getoption("flaptastic_key"):
            send_flap(item, call)


def send_flap(item, call):
    key = item.session.config.getoption("flaptastic_key")
    commit_id = item.session.config.getoption("commit_id")
    branch = item.session.config.getoption("branch")
    flaptastic_secret = item.session.config.getoption("flaptastic_secret")
    host = "api.flaptastic.com"
    port = 6789
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = {
        "exception": str(call.excinfo.value),
        "file": item.location[0],
        "name": item.name,
        "line": call.excinfo.traceback[len(call.excinfo.traceback)-1].lineno,
        "commit_id": commit_id,
        "branch": branch
    }
    ts = int(time.time())
    document = {
        "key": key,
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
