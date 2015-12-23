import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="sourgraph",
    version="0.1.0",
    author="ege",
    author_email="",
    description=("sourgraph"),
    license="BSD",
    keywords="eksi sour graph",
    url="https://github.com/egemenyildiz/sourgraph",
    packages=['sourgraph'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
)
