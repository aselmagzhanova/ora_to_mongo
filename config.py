ora_user = 'system'
ora_password = ''
ora_ip = ''
ora_port = 1521
sid = ''

mongodb_conn_string = 'mongodb://mongo_rw:mongo_rw@localhost:27017/'
mongodb_db = 'db1'
mongodb_collection = 'test1'
sql_query = u"SELECT ID FROM FKS_SAVEPOINTS.DOCUMENT "
sql_get_data = u"SELECT DOCUMENT_IDENTIFIER, BODY FROM FKS_SAVEPOINTS.DOCUMENT where id = :1"
sql_update_uid = "UPDATE FKS_SAVEPOINTS.DOCUMENT SET NOSQL_UID = :1 where id = :2"
num_rows_fetch = 5

