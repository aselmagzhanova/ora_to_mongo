import cx_Oracle
from oracle_to_mongo import config
from pymongo import MongoClient
import gridfs
from datetime import datetime
from multiprocessing import Process

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

def migrate(thread_num: int):

    error_exception = None

    try:
        oracle_conn = create_ora_conn(config.ora_user, config.ora_password, config.ora_ip, config.ora_port, config.sid)
        mongodb_client, mongodb_db = create_mongo_conn(config.mongodb_conn_string, config.mongodb_db)
        cursor_bounds = oracle_conn.cursor()
        cursor_bounds.execute(config.sql_get_bounds, [thread_num])
        start_id, end_id = cursor_bounds.fetchone()
        cursor_bounds.close()
        fs = gridfs.GridFS(mongodb_db, collection='nrgEvent', disable_md5=True)
        cursor = oracle_conn.cursor()
        cursor.execute(config.sql_query, [start_id, end_id])
        id, document_identifier, data = cursor.fetchone()
        while (id is not None):
            _id = fs.put(filename=document_identifier, data=data.read(), metadata={"documentType": "nrgEvent"})
            uid_update(str(_id), id, oracle_conn)
            id, document_identifier, data = cursor.fetchone()
        cursor.close()
        close_ora_conn(oracle_conn)
        close_mongo_conn(mongodb_client)
    except cx_Oracle.Error as error:
        error_exception = error
        print(error_exception)

def uid_update(_id: str, id: int, oracle_conn):
    cursor_upd = oracle_conn.cursor()
    cursor_upd.execute(config.sql_update_uid, [_id, id])
    oracle_conn.commit()
    cursor_upd.close()
    return cursor_upd

if __name__ == '__main__':

    startTime = datetime.now()

    procs = []

    for i in range(config.num_threads):
        proc = Process(target=migrate, args=(i,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()


    endTime = datetime.now()
    print ("Время выполнения: ", endTime - startTime)


