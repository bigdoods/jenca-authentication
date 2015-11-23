from setuptools import setup, find_packages

# We use requirements.txt files instead of just declaring the requirements here
# because this helps with Docker package caching.
with open("requirements.txt") as requirements:
    install_requires = requirements.readlines()

setup(
    name="Jenca_Authentication",
    version="0.1",
    description="Authenticate users for Jenca Cloud.",
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={
        "dev": [
            # Allows us to measure code coverage:
            "coverage",
            # Style check documentation:
            "doc8",
            # Code analysis tool with linting:
            "flake8",
            # Build documentation:
            "Sphinx",
            # Describe RESTful HTTP APIs in Sphinx:
            "sphinxcontrib-httpdomain",
        ],
    },
)
