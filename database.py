import mysql.connector as mysql

INSERT_ACCOUNT = "INSERT INTO accounts (name, username, password) VALUES (%s, %s, %s, %s)"


class AccountDatabase:

    def __init__(self, host, name, password):
        self.db = mysql.connect(
            host=host,
            user=name,
            password=password)

        self.query = ''
        self.cursor = self.db.cursor()
        self.values = None

    def set_query(self, query):
        self.query = query

    def get_query(self):
        return self.query

    def create_database(self, database_name):
        self.cursor.execute(f"DROP DATABASE {database_name};")
        self.cursor.execute(f"CREATE DATABASE {database_name}")
        self.cursor.execute(f"USE {database_name};")

    def create_table(self):
        # TODO: Revisit this
        self.cursor.execute(self.query)

    def get_values(self):
        return self.values

    def set_values(self, values):
        self.values = values

    def select_all_from_table(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        results = self.cursor.fetchall()
        for result in results:
            print(result)

    def custom_command(self, query):
        self.cursor.execute(f"{query}")
        results = self.cursor.fetchall()
        for result in results:
            return result

    def insert_record(self, query):
        self.cursor.execute(f"{query}")
        self.db.commit()

    def insert_many_records(self):
        self.cursor.executemany(self.query, self.values)
        self.db.commit()
        print(f"{self.cursor.rowcount} tuples inserted")