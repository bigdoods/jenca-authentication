from setuptools import setup, find_packages

# We use requirements.txt instead of just declaring the requirements here
# because this helps with Docker package caching.
with open("requirements.txt") as requirements:
    install_requires = requirements.readlines()

# We use dev-requirements.txt instead of just declaring the requirements here
# because Read The Docs needs a requirements file.
with open("dev-requirements.txt") as dev_requirements:
    dev_requires = dev_requirements.readlines()

setup(
    name="Jenca_Authentication",
    version="0.1",
    description="Authenticate users for Jenca Cloud.",
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={
        "dev": dev_requires,
    },
)
