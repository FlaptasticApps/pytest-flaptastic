"""
A pytest plugin which helps tracking flappy tests.
"""
import socket

# ############### pytest hooks ################


def pytest_addoption(parser):
    group = parser.getgroup('flaptastic')
    group._addoption('--flaptastic-key',
                     action='store', type=str, dest='flaptastic_key',
                     default=None, help='Flaptastic private project secret')


def pytest_runtest_makereport(item, call):
    if call.excinfo is not None:
        if item.session.config.getoption("flaptastic_key"):
            send_flap(item, call)


def send_flap(item, call):
    key = item.session.config.getoption("flaptastic_key")
    host = "api.flaptastic.com"
    port = 6789
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = "something flapped. key = {}".format(key)
    client_sock.sendto(message.encode(), (host, port))
