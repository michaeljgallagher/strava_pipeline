# test_postgres.py
import tempfile
from unittest.mock import MagicMock

import pytest
from strava_pipeline.utils.postgres import get_most_recent, push_csv_to_postgres, push_last_start_date


@pytest.fixture
def mock_conn():
    conn = MagicMock()
    cursor = MagicMock()
    conn.cursor.return_value = cursor
    return conn


def test_push_csv_to_postgres(mock_conn):
    temppath = tempfile.NamedTemporaryFile().name
    table_name = "test_table"
    with open(temppath, "w") as f:
        f.write("col1,col2\n1,a\n2,b\n3,c\n")
    push_csv_to_postgres(mock_conn, temppath, table_name)
    mock_conn.commit.assert_called_once()
    mock_conn.cursor.assert_called_once()
    mock_conn.rollback.assert_not_called()


def test_get_most_recent(mock_conn):
    table_name = "test_table"
    col_name = "col1"
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchone.return_value = (3,)
    assert get_most_recent(mock_conn, table_name, col_name) == 3
    mock_cursor.execute.assert_called_with(f"SELECT MAX({col_name}) FROM {table_name}")
    mock_conn.cursor.assert_called_once()
    mock_conn.rollback.assert_not_called()


def test_push_last_start_date(mock_conn):
    start_date = 1620272700  # May 6, 2021, 00:01:40 UTC
    table_name = "test_table"
    col_name = "col1"
    push_last_start_date(mock_conn, start_date, table_name, col_name)
    mock_conn.commit.assert_called_once()
    mock_conn.cursor.assert_called_once()
    mock_conn.rollback.assert_not_called()
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.execute.assert_called_with(
        f"""INSERT INTO {table_name} ({col_name}) VALUES ({start_date})"""
    )
