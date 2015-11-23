from setuptools import setup, find_packages

setup(
    name="Jenca_Authentication",
    version="0.1",
    description="Authenticate users for Jenca Cloud.",
    packages=find_packages(),
    install_requires=[
        'Flask==0.10.1',
        'Flask-Login==0.3.2',
        'Flask-Bcrypt==0.7.1',
        'Flask-SQLAlchemy==2.1',
        'requests==2.8.1',
    ],
    extras_require={
        "dev": [
            # Allows us to measure code coverage:
            "coverage",
            # Code analysis tool with linting:
            "flake8",
            # Build documentation:
            "Sphinx",
        ],
    },
)
