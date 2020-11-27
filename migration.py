import cx_Oracle
from oracle_to_mongo import config
from pymongo import MongoClient
import gridfs
from datetime import datetime
from multiprocessing import Pool

def create_ora_conn(ora_user: str,
                    ora_password: str,
                    ora_ip: str,
                    ora_port: int,
                    sid: str):
    ## create connections
    # create oracle connection
    try:
        dsn_tns = cx_Oracle.makedsn(ora_ip, ora_port, sid)
        oracle_conn = cx_Oracle.connect(ora_user, ora_password, dsn_tns)
    except:
        raise Exception("could not create a connection to Oracle database")
    return oracle_conn


def create_mongo_conn(mongodb_conn_string: str,
                      mongodb_db: str):

    # create mongodb connection
    try:
        mongodb_client = MongoClient(mongodb_conn_string)
        mongodb_db = mongodb_client[mongodb_db]
    except:
        raise Exception("could not create a connection to MongoDB server / database")
    return mongodb_client, mongodb_db

def close_ora_conn(oracle_conn):
    if oracle_conn is not None:
        oracle_conn.close()

def close_mongo_conn(mongodb_client):
    if mongodb_client is not None:
        mongodb_client.close()

def migrate(id: int):

    error_exception = None

    try:
        oracle_conn_cur = create_ora_conn(config.ora_user, config.ora_password, config.ora_ip, config.ora_port, config.sid)
        mongodb_client, mongodb_db = create_mongo_conn(config.mongodb_conn_string, config.mongodb_db)
        cursor_cur = oracle_conn_cur.cursor()
        cursor_cur.execute(config.sql_get_data, [id])
        document_identifier, data = cursor_cur.fetchone()
        fs = gridfs.GridFS(mongodb_db, collection='nrgEvent', disable_md5=True)
        _id = fs.put(filename=document_identifier, data=data.read(), metadata={"documentType": "nrgEvent"})
        uid_update(str(_id), id, oracle_conn_cur)
        cursor_cur.close()
        close_ora_conn(oracle_conn_cur)
        close_mongo_conn(mongodb_client)
    except cx_Oracle.Error as error:
        error_exception = error
        print(error_exception)

def uid_update(_id: str, id: int, oracle_conn_cur):
    cursor_upd = oracle_conn_cur.cursor()
    cursor_upd.execute(config.sql_update_uid, [_id, id])
    oracle_conn_cur.commit()
    cursor_upd.close()

if __name__ == '__main__':

    startTime = datetime.now()

    oracle_conn = create_ora_conn(config.ora_user,
                                  config.ora_password,
                                  config.ora_ip,
                                  config.ora_port,
                                  config.sid)
    cursor = oracle_conn.cursor()
    cursor.execute(config.sql_query)
    rows = cursor.fetchmany(config.num_rows_fetch)
    while len(rows) > 0:
        # fetch next rows
        ids = [row[0] for row in rows]
        pool = Pool(4)
        results = pool.map(migrate, ids)
        pool.close()
        pool.join()
        rows = cursor.fetchmany(config.num_rows_fetch)

    cursor.close()
    endTime = datetime.now()
    print ("Время выполнения: ", endTime - startTime)

    close_ora_conn(oracle_conn)


'''
#one thread working
    cursor = oracle_conn.cursor()
    cursor.execute(config.sql_query)
    rows = cursor.fetchall()
    ids = [row[0] for row in rows]
    for id in ids:
        migrate(id)
'''