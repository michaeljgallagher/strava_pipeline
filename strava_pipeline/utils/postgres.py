import psycopg2


def push_csv_to_postgres(
    conn: psycopg2.extensions.connection, csv_path: str, table_name: str
) -> None:
    """
    Pushes the data from a CSV file to a PostgreSQL table.

    :param conn: The PostgreSQL connection object.
    :param csv_path: The path to the CSV file.
    :param table_name: The name of the PostgreSQL table.
    """
    with open(csv_path) as file:
        cursor = conn.cursor()
        next(file)  # SKIP HEADERS
        cursor.copy_from(file, table_name, sep="\u0001", null="")
        conn.commit()
    cursor.close()


def get_most_recent(
    conn: psycopg2.extensions.connection, table_name: str, col_name: str
) -> any:
    """
    Retrieves the most recent value from a column in a PostgreSQL table.

    :param conn: The PostgreSQL connection object.
    :param table_name: The name of the PostgreSQL table.
    :param col_name: The name of the column.
    :return: The most recent value in the specified column.
    :raises RuntimeError: If there is an error retrieving the value.
    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT MAX({col_name}) FROM {table_name}")
    res = cursor.fetchone()[0]
    cursor.close()
    return res


def push_last_start_date(
    conn: psycopg2.extensions.connection,
    start_date: int,
    table_name: str,
    col_name: str,
) -> None:
    """
    Pushes the last start date to a column in a PostgreSQL table.

    :param conn: The PostgreSQL connection object.
    :param start_date: The start date to push.
    :param table_name: The name of the PostgreSQL table.
    :param col_name: The name of the column.
    """
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO {table_name} ({col_name}) VALUES ({start_date})""")
    conn.commit()
    cursor.close()
