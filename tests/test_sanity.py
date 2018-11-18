import os
from argparse import Namespace
from pytest_flaptastic.plugin import option_to_env_name
from pytest_flaptastic.plugin import get_option
from pytest_flaptastic.plugin import missing_options_detected
from pytest_flaptastic.plugin import param_map
from unittest import mock


def test_option_parsing():
    namespace = Namespace(foo="bar")
    assert "bar" == get_option(namespace, "foo")


def test_option_to_env_name():
    assert "HELLO_WORLD" == option_to_env_name("hello-world")


@mock.patch.dict(os.environ, {'COLOR': 'blue'})
def test_get_option_works_with_env_vars():
    namespace = Namespace()
    assert "blue" == get_option(namespace, "color")


@mock.patch.dict(os.environ, {'COLOR': 'blue'})
def test_get_option_prefers_cli_params():
    namespace = Namespace(color="red")
    assert "red" == get_option(namespace, "color")


def test_no_missing_options_detected_when_all_are_passed():
    assert not missing_options_detected(
        Namespace(**param_map)
    )


def test_missing_options_detected_when_none_are_passed():
    assert missing_options_detected(
        Namespace(**{})
    )


# def test_simple_assertion2():
#     assert True
#
#
# def test_simple_assertion3():
#     assert False
#
#
# def test_simple_assertion4():
#     assert True
#
#
# def test_simple_assertion5():
#     assert True
