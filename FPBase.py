import sqlite3

class Dbase:
    _conn = None
    _cursor = None

    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        self._conn = sqlite3.connect(self.db_name)
        self._cursor = self._conn.cursor()

    def execute(self, sql_string):
        self._cursor.executescript(sql_string)

    # nothing else should influence the cursor hence only a get class not a set class
    @property
    def get_cursor(self):
        return self._cursor

    @property
    def get_connection(self):
        return self._conn

    def reset_database(self):
        raise NotImplementedError()

    def close_db(self):
        self._conn.close()
