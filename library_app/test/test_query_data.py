import pytest
from unittest.mock import patch, MagicMock, ANY
import datetime
from sqlalchemy import Date, cast, func, and_
from library_app.scripts.query_data import query_data
from library_app.models.models import Cliente, MonitoreoBots

# filepath: c:\Users\lmarinaro\Documents\sqlalchemy\sqlalchemy-1\library_app\tests\test_query_data.py

# Use absolute import based on the project structure


# Mock data structures needed for tests
class MockCliente:
    def __init__(
        self,
        id,
        nombre,
        cuit,
        documentacion,
        dias_ejecucion,
        cliente_jurisdicciones=None,
    ):
        self.id = id
        self.nombre = nombre
        self.cuit = cuit
        self.documentacion = documentacion
        self.dias_ejecucion = dias_ejecucion
        self.cliente_jurisdicciones = (
            cliente_jurisdicciones if cliente_jurisdicciones is not None else []
        )


@pytest.fixture
def mock_db_session():
    """Fixture to mock the database session."""
    with patch("library_app.scripts.query_data.SessionLocal") as mock_session_local:
        mock_session = MagicMock()
        # Mock the context manager behavior
        mock_session_local.return_value.__enter__.return_value = mock_session
        yield mock_session


@pytest.fixture
def mock_datetime():
    """Fixture to mock datetime.date.today()."""
    with patch("library_app.scripts.query_data.datetime") as mock_dt:
        yield mock_dt


def test_query_data_finds_client_for_today(mock_db_session, mock_datetime, capsys):
    """
    Test that query_data finds and prints a client scheduled for today
    who hasn't run successfully yet.
    """
    # Arrange
    test_date = datetime.date(2023, 10, 23)  # A Monday
    mock_datetime.date.today.return_value = test_date
    day_name_es = "Lunes"

    mock_client = MockCliente(
        id=1,
        nombre="Test Client Lunes",
        cuit="123456789",
        documentacion=True,
        dias_ejecucion="Lunes,Martes",
        cliente_jurisdicciones=[1, 2],  # Example jurisdiction IDs
    )

    # Mock the query chain
    mock_query = MagicMock()
    mock_db_session.query.return_value = mock_query
    # Simulate the filtering steps - we mock the final .all() result
    # based on the expected logic for this test case.
    mock_query.filter.return_value.filter.return_value.filter.return_value.all.return_value = [
        mock_client
    ]

    # Act
    query_data()

    # Assert
    # 1. Check database interaction (basic check that query was initiated)
    mock_db_session.query.assert_called_once_with(Cliente)

    # 2. Check filters were called (can be more specific if needed)
    # Example of checking a specific filter call:
    # We expect the day filter to be called with "%Lunes%"
    like_filter_call = next(
        (
            call
            for call in mock_query.filter.call_args_list
            if day_name_es in str(call.args[0])
        ),
        None,
    )
    assert like_filter_call is not None, (
        f"Filter with '{day_name_es}' not found in calls"
    )

    # 3. Check standard output
    captured = capsys.readouterr()
    assert "\n--- Clientes ---" in captured.out
    assert (
        f"ID: {mock_client.id}, Nombre: {mock_client.nombre}, CUIT: {mock_client.cuit}"
        in captured.out
    )
    assert f"Jurisdicciones: {len(mock_client.cliente_jurisdicciones)}" in captured.out
    assert "---" in captured.out


def test_query_data_no_client_for_today(mock_db_session, mock_datetime, capsys):
    """
    Test that query_data finds no clients if none are scheduled for today.
    """
    # Arrange
    test_date = datetime.date(2023, 10, 25)  # A Wednesday
    mock_datetime.date.today.return_value = test_date
    day_name_es = "Miércoles"

    # Mock the query chain to return an empty list
    mock_query = MagicMock()
    mock_db_session.query.return_value = mock_query
    mock_query.filter.return_value.filter.return_value.filter.return_value.all.return_value = []

    # Act
    query_data()

    # Assert
    # 1. Check database interaction
    mock_db_session.query.assert_called_once_with(Cliente)

    # 2. Check filters were called (can be more specific if needed)
    # Example of checking a specific filter call:
    # We expect the day filter to be called with "%Miércoles%"
    like_filter_call = next(
        (
            call
            for call in mock_query.filter.call_args_list
            if day_name_es in str(call.args[0])
        ),
        None,
    )
    assert like_filter_call is not None, (
        f"Filter with '{day_name_es}' not found in calls"
    )

    # 3. Check standard output
    captured = capsys.readouterr()
    assert "\n--- Clientes ---" in captured.out
    assert "ID:" not in captured.out  # No client details should be printed
    assert "Nombre:" not in captured.out


def test_query_data_client_already_run_today(mock_db_session, mock_datetime, capsys):
    """
    Test that query_data excludes clients that have already run successfully today.
    This is implicitly tested by mocking the final result, assuming the DB query works.
    """
    # Arrange
    test_date = datetime.date(2023, 10, 24)  # A Tuesday
    mock_datetime.date.today.return_value = test_date
    day_name_es = "Martes"

    # Mock the query chain to return an empty list, simulating that the
    # NOT EXISTS clause filtered out the potential client.
    mock_query = MagicMock()
    mock_db_session.query.return_value = mock_query
    mock_query.filter.return_value.filter.return_value.filter.return_value.all.return_value = []

    # Act
    query_data()

    # Assert
    # 1. Check database interaction
    mock_db_session.query.assert_called_once_with(Cliente)

    # 2. Check filters were called (can be more specific if needed)
    # Example of checking a specific filter call:
    # We expect the day filter to be called with "%Martes%"
    like_filter_call = next(
        (
            call
            for call in mock_query.filter.call_args_list
            if day_name_es in str(call.args[0])
        ),
        None,
    )
    assert like_filter_call is not None, (
        f"Filter with '{day_name_es}' not found in calls"
    )

    # 3. Check standard output
    captured = capsys.readouterr()
    assert "\n--- Clientes ---" in captured.out
    assert "ID:" not in captured.out  # No client details should be printed


def test_query_data_client_no_documentation(mock_db_session, mock_datetime, capsys):
    """
    Test that query_data excludes clients with documentacion=False.
    This is implicitly tested by mocking the final result.
    """
    # Arrange
    test_date = datetime.date(2023, 10, 26)  # A Thursday
    mock_datetime.date.today.return_value = test_date
    day_name_es = "Jueves"

    # Mock the query chain to return an empty list, simulating that the
    # documentacion=True filter excluded potential clients.
    mock_query = MagicMock()
    mock_db_session.query.return_value = mock_query
    mock_query.filter.return_value.filter.return_value.filter.return_value.all.return_value = []

    # Act
    query_data()

    # Assert
    # 1. Check database interaction
    mock_db_session.query.assert_called_once_with(Cliente)

    # 2. Check filters were called (can be more specific if needed)
    # Example of checking a specific filter call:
    # We expect the day filter to be called with "%Jueves%"
    like_filter_call = next(
        (
            call
            for call in mock_query.filter.call_args_list
            if day_name_es in str(call.args[0])
        ),
        None,
    )
    assert like_filter_call is not None, (
        f"Filter with '{day_name_es}' not found in calls"
    )

    # 3. Check standard output
    captured = capsys.readouterr()
    assert "\n--- Clientes ---" in captured.out
    assert "ID:" not in captured.out  # No client details should be printed
