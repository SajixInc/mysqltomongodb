import json
from message import prettyprint, MsgType

delete_existing_documents = True
table_count_e = []
table_count_s = []


def migrate_table(db, table_name, mydb):
    # TODO: Sanitize table name to conform to MongoDB Collection naming restrictions
    # For example, the $ sign is allowed in MySQL table names but not in MongoDB Collection names
    mycursor = db.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM " + table_name + ";")
    myresult = mycursor.fetchall()

    mycol = mydb[table_name]

    # insert the documents
    if len(myresult) == 0:
        mycol = mydb[table_name]
        mycol.create_index("ID", unique=True)
        table_count_s.append(table_name)
        prettyprint(f"{table_name} is empty table number", MsgType.OKGREEN)
        return mycol
    elif len(myresult) > 0:
        table_count_s.append(table_name)
        y = json.loads(json.dumps(myresult, default=str, indent=4, sort_keys=True))
        # print(type(y))
        # data = str(myresult)
        # print(myresult)
        x = mycol.insert_many(y)
        return len(x.inserted_ids)
    else:
        return 0
