'''
################################## server.py #############################
# Lab1 gRPC RocksDB Server 
################################## server.py #############################
'''
import time
import grpc
import datastore_pb2
import datastore_pb2_grpc
import uuid
import rocksdb
import random

from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

master_already_stored_requests = []

class MyDatastoreServicer(datastore_pb2.DatastoreServicer):
    def __init__(self):
        self.db = rocksdb.DB("assignment2_master.db", rocksdb.Options(create_if_missing=True))

    def put(self, request, context):
        print("put")
        key = uuid.uuid4().hex
        # TODO - save key and value into DB converting request.data string to utf-8 bytes
        self.db.put(bytes(key, encoding="UTF-8"), bytes(request.data, encoding="UTF-8"))

        return datastore_pb2.Response(data=key)

    def get(self, request, context):
        print("get")
        # TODO - retrieve the value from DB by the given key. Needs to convert request.data string to utf-8 bytes. 
        value = self.db.get(bytes(request.data, encoding="UTF-8"))

        return datastore_pb2.Response(data=value)

    def replicator_put(self, requests, context):
        for request in requests:
            print("put (streaming): " + request.data)
            key = uuid.uuid4().hex
            self.db.put(bytes(key, encoding="UTF-8"), bytes(request.data, encoding="UTF-8"))
            master_already_stored_requests.append(datastore_pb2.Request(data=bytes(key, encoding="UTF-8")))
            yield datastore_pb2.Response(data=key)

    def replicator(self, requests, context):
        for key in master_already_stored_requests:
            yield key
            time.sleep(random.uniform(1, 2))
        master_already_stored_requests.clear();


def run(host, port):
    '''
    Run the GRPC server
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    datastore_pb2_grpc.add_DatastoreServicer_to_server(MyDatastoreServicer(), server)
    server.add_insecure_port('%s:%d' % (host, port))
    server.start()

    try:
        while True:
            print("Server started at...%d" % port)
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run('0.0.0.0', 3000)