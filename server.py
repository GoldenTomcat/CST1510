from TCP import Server
from database import AccountDatabase


def main():
    accounts = AccountDatabase('localhost', 'root', '1234')
    accounts.create_database('accounts')
    # TODO: Limit accounts in gui to params of the sql table i.e max 20 char for name
    create_table_accounts = "CREATE TABLE Account(name VARCHAR(20), username VARCHAR(20) NOT NULL, " \
                            "password VARCHAR (20) NOT NULL);"

    accounts.set_query(create_table_accounts)
    print(accounts.get_query())

    accounts.create_table()

    # accounts.custom_command("SHOW DATABASES")


if __name__ == '__main__':
    server = Server('localhost', 5000, 1024)
    main()
    server.run()
