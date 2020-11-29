ora_user = 'system'
ora_password = '*'
ora_ip = '*.*.*.*'
ora_port = 1521
sid = '*'

mongodb_conn_string = 'mongodb://mongo_rw:mongo_rw@localhost:27017/'
mongodb_db = 'db1'
mongodb_collection = 'test1'
sql_query = u"SELECT ID, DOCUMENT_IDENTIFIER, BODY FROM FKS_SAVEPOINTS.DOCUMENT where NOSQL_UID is null and id between :1 and :2"
sql_get_bounds = u"SELECT start_id, end_id FROM FKS_SAVEPOINTS.DOCUMENT_MIGRATE_BOUNDS where thread_id = :1"
sql_update_uid = "UPDATE FKS_SAVEPOINTS.DOCUMENT SET NOSQL_UID = :1 where id = :2"
num_rows_fetch = 5
num_threads = 5

