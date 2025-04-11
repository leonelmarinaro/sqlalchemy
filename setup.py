from setuptools import setup, find_packages

setup(
    name="library_app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy",
        "alembic",
        "python-dotenv",
        "psycopg2-binary",
    ],
)
