import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="sourgraph",
    version="0.1.2",
    author="ege",
    author_email="egemenyildiz.e@gmail.com",
    description=("sourgraph"),
    license="BSD",
    keywords="eksisozluk sour graph",
    url="https://github.com/egemenyildiz/sourgraph",
    packages=['sourgraph', 'sourgraph/web'],
    scripts=['sourgraph/sourgraph'],
    long_description=read('README.md'),
    install_requires=[
        'BeautifulSoup==3.2.1',
        'eventlet==0.17.4',
        'greenlet==0.4.9',
        'matplotlib==1.4.3',
        'numpy==1.10.0.post2',
        'progressbar==2.3',
        'requests==2.8.0',
        'ndg-httpsclient==0.4.0',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
)
