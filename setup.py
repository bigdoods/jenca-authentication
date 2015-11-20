import uuid

from pip.req import parse_requirements
from setuptools import setup, find_packages

setup(
    name="Jenca_Authentication",
    version="0.1",
    description="Authenticate users for Jenca Cloud.",
    packages=find_packages(),
    install_requires=[str(requirement.req) for requirement in
                      parse_requirements('requirements.txt',
                          session=uuid.uuid1())],
)
