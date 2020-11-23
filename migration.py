import cx_Oracle
from oracle_to_mongo import config
from pymongo import MongoClient
import gridfs

def export_data_from_oracle_to_mongodb(ora_user: str,
                                       ora_password: str,
                                       ora_ip: str,
                                       ora_port: int,
                                       sid: str,
                                       mongodb_conn_string: str,
                                       mongodb_db: str,
                                       sql_query: str):
    error_exception = None

    ## create connections
    # create oracle connection
    try:
        dsn_tns = cx_Oracle.makedsn(ora_ip, ora_port, sid)
        oracle_conn = cx_Oracle.connect(ora_user, ora_password, dsn_tns)
    except:
        raise Exception("could not create a connection to Oracle database")

    # create mongodb connection
    try:
        mongodb_client = MongoClient(mongodb_conn_string)
        mongodb_db = mongodb_client[mongodb_db]
    except:
        # if an error ocurred while creating the connection to mongodb, oracle connection would be already created
        # we need to destroy it
        if oracle_conn is not None:
            oracle_conn.close()
        if mongodb_client is not None:
            mongodb_client.close()
        raise Exception("could not create a connection to MongoDB server / database")

    ## exporting data
    try:
        cursor = oracle_conn.cursor()
        print('executing the query in Oracle server...')
        cursor.execute(sql_query)
        fs = gridfs.GridFS(mongodb_db)
        for record in cursor.fetchall():
            a = fs.put(document_identifier=record[0], data=record[1])

    except cx_Oracle.Error as error:
        error_exception = error

    finally:
        cursor.close()
        oracle_conn.close()
        mongodb_client.close()

if __name__ == '__main__':
    export_data_from_oracle_to_mongodb(config.ora_user,
                                       config.ora_password,
                                       config.ora_ip,
                                       config.ora_port,
                                       config.sid,
                                       config.mongodb_conn_string,
                                       config.mongodb_db,
                                       config.sql_query)

