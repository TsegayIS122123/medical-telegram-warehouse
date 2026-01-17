"""Test that all required packages can be imported."""
import pytest

def test_import_telethon():
    import telethon
    assert hasattr(telethon, '__version__')

def test_import_dbt():
    # dbt has version in different location
    import dbt.version
    assert hasattr(dbt.version, '__version__')

def test_import_fastapi():
    import fastapi
    assert hasattr(fastapi, '__version__')

def test_import_dagster():
    import dagster
    assert hasattr(dagster, '__version__')

def test_import_sqlalchemy():
    import sqlalchemy
    assert hasattr(sqlalchemy, '__version__')

def test_import_pandas():
    import pandas
    assert hasattr(pandas, '__version__')
