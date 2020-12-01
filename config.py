ora_user = 'system'
ora_password = 'WVh1bXl1qQNk'
ora_ip = '192.168.231.55'
ora_port = 1521
sid = 'busdb'

mongodb_conn_string = 'mongodb://mongo_rw:mongo_rw@localhost:27017/'
mongodb_db = 'db1'
sql_query = u"SELECT ID, DOCUMENT_IDENTIFIER, BODY FROM FKS_SAVEPOINTS.DOCUMENT where NOSQL_UID is null and id between :1 and :2"
sql_get_bounds = u"SELECT start_id, end_id FROM FKS_SAVEPOINTS.DOCUMENT_MIGRATE_BOUNDS where thread_id = :1"
sql_update_uid = "UPDATE FKS_SAVEPOINTS.DOCUMENT SET NOSQL_UID = :1 where id = :2"
num_threads = 5


#PAK
#ora_password = 'yMZQgfvMzbAwq0AW'
#ora_ip = '10.141.84.62'
#sid = 'fksbusdb'


#mongodb_conn_string = 'mongodb://mongo_rw:mongo_rw@eis-mongo-gisnr01.eis3.fk.dks.lanit.ru:26000/'
#mongodb_db = 'BUS_STORAGE'