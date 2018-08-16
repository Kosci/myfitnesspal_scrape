import sqlite3


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except ValueError as e:
        print(e)

    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except ValueError as e:
        print(e)


def create_db():
    mfp_data_table = """ CREATE TABLE IF NOT EXISTS mfp_data (
                                        date text PRIMARY KEY,
                                        weight text NULL,
                                        waist text,
                                        calories text
                                    ); """

    sqlite_file = 'mfp_db.sqlite'  # name of the sqlite database file
    conn = create_connection(sqlite_file)

    if conn is not None:
        # create projects table
        create_table(conn, mfp_data_table)

        # Committing changes and closing the connection to the database file
        conn.commit()
        conn.close()
    else:
        print("Error! cannot create the database connection.")

def create_entry(date, weight, waist, calories):
    sqlite_file = 'mfp_db.sqlite'
    conn = create_connection(sqlite_file)
    params = (date, weight, waist, calories)
    conn.execute('INSERT INTO mfp_data VALUES (?, ?, ?, ?)', params)
    # Committing changes and closing the connection to the database file
    conn.commit()
    conn.close()







