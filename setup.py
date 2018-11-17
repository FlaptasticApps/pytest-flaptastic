import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytest-flaptastic",
    version="0.0.7",
    author="Jonathan Block",
    author_email="block.jon@gmail.com",
    description="Flaptastic py.test plugin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blockjon/pytest-flaptastic",
    packages=setuptools.find_packages(),
    entry_points={"pytest11": ["name_of_plugin = pytest_flaptastic.plugin"]},
    classifiers=[
        "Framework :: Pytest",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
