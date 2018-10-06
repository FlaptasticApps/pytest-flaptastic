from setuptools import setup

setup(
    name='pytest-flaptastic',
    packages=['pytest_flaptastic'],
    entry_points={"pytest11": ["name_of_plugin = pytest_flaptastic.plugin"]},
    # custom PyPI classifier for pytest plugins
    classifiers=["Framework :: Pytest"],
)
