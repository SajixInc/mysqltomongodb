import mysql.connector
import pymongo
import datetime
from message import prettyprint, MsgType
from migrate import migrate_table



def connection(mysql_data, mongo_data, user, password):
    begin_time = datetime.datetime.now()
    abort = False
    prettyprint(f"Script started at: {begin_time}", MsgType.HEADER)

    delete_existing_documents = True;
    mysql_host = "localhost"
    mysql_database = mysql_data
    mysql_schema = mysql_data
    mysql_user = user
    mysql_password = password

    mongodb_host = "mongodb://localhost:27017/"
    mongodb_dbname = mongo_data

    '''if (delete_existing_documents):
        confirm_delete = input("Delete existing documents from collections (y)es/(n)o/(a)bort?")
        if confirm_delete.lower() == "a":
            abort = True
        elif confirm_delete.lower() == "n":
            delete_existing_documents = False
        else:
            # Confirm again
            confirm_delete = input("Are you sure (y)es/(n)?")
            if confirm_delete.lower() == "y":
                delete_existing_documents = True
            else:
                abort = True'''

    if abort:
        prettyprint("Script aborted by user", MsgType.FAIL)
    else:
        '''if (delete_existing_documents):
            prettyprint("Existing documents will be deleted from collections", MsgType.FAIL)
        else:
            prettyprint("Existing documents will not be deleted from collections", MsgType.OKGREEN)'''

        # MySQL connection
        prettyprint("Connecting to MySQL server...", MsgType.HEADER)
        mysqldb = mysql.connector.connect(
            host=mysql_host,
            database=mysql_database,
            user=mysql_user,
            password=mysql_password
        )
        prettyprint("Connection to MySQL Server succeeded.", MsgType.OKGREEN)

        # MongoDB connection
        prettyprint("Connecting to MongoDB server...", MsgType.HEADER)
        myclient = pymongo.MongoClient(mongodb_host)
        mydb = myclient[mongodb_dbname]
        prettyprint("Connection to MongoDB Server succeeded.", MsgType.OKGREEN)

        # Start migration
        prettyprint("Migration started...", MsgType.HEADER)

        dblist = myclient.list_database_names()
        if mongodb_dbname in dblist:
            prettyprint("The database exists.", MsgType.OKBLUE)
        else:
            prettyprint("The database does not exist, it is being created.", MsgType.WARNING)

        # Iterate through the list of tables in the schema
        table_list_cursor = mysqldb.cursor()
        table_list_cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = %s ORDER BY table_name LIMIT 1000;",
            (mysql_schema,))
        tables = table_list_cursor.fetchall()

        total_count = len(tables)
        success_count = 0
        fail_count = 0

        for table in tables:
            try:
                prettyprint(f"Processing table: {table[0]}...", MsgType.OKCYAN)
                inserted_count = migrate_table(mysqldb, table[0], mydb)
                success_count += 1
                prettyprint(f"Processing table: {table[0]} completed. {inserted_count} documents inserted.",
                            MsgType.OKGREEN)
            except Exception as e:
                fail_count += 1
                prettyprint(f"{e}", MsgType.FAIL)

        prettyprint("Migration completed.", MsgType.HEADER)
        prettyprint(f"{success_count} of {total_count} tables migrated successfully.", MsgType.OKGREEN)
        if fail_count > 0:
            prettyprint(f"Migration of {fail_count} tables failed. See errors above.", MsgType.FAIL)

    end_time = datetime.datetime.now()
    prettyprint(f"Script completed at: {end_time}", MsgType.HEADER)
    prettyprint(f"Total execution time: {end_time - begin_time}", MsgType.HEADER)
    migration = mydb.command("dbstats")

    prettyprint(f"No of Collections {mongo_data}: {migration['collections']}", MsgType.HEADER)
