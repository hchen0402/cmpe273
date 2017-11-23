'''
################################## client.py #############################
# 
################################## client.py #############################
'''
import grpc
import datastore_pb2
import argparse
import random
import time
import rocksdb

PORT = 3000

current_values = []

class DatastoreClient():
    def __init__(self, host='0.0.0.0', port=PORT):
        self.db = rocksdb.DB("assignment2_follower.db", rocksdb.Options(create_if_missing=True))
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = datastore_pb2.DatastoreStub(self.channel)

    def put(self, value):
        return self.stub.put(datastore_pb2.Request(data=value))

    def get(self, key):
        return self.stub.get(datastore_pb2.Request(data=key))

    def replicator_put(self, requests):
        return self.stub.replicator_put(requests)

    def replicator(self):
        responses = self.stub.replicator(datastore_pb2.Request())
        i = 0
        for response in responses:
            print("{%s : %s} has been stored in the follower's DB." % (response.data, current_values[i]))
            self.db.put(bytes(response.data, encoding="UTF-8"), bytes(current_values[i], encoding="UTF-8"))
            i += 1
        current_values.clear();


def create_request(value):
    return datastore_pb2.Request(data=value);


def generate_requests():
    requests = [create_request('foo'), create_request('bar'), create_request('hello'), create_request('world')]

    for request in requests:
        print("\n## PUT Request: value = " + request.data)
        current_values.append(request.data)
        yield request
        time.sleep(random.uniform(1, 2))


def generate_requests_again():
    requests = [create_request('This'), create_request('is'), create_request('cmpe273')]

    for request in requests:
        print("\n## PUT Request: value = " + request.data)
        current_values.append(request.data)
        yield request
        time.sleep(random.uniform(1, 2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="display a square of a given number")
    args = parser.parse_args()
    print("Client is connecting to Server at {}:{}...".format(args.host, PORT))
    client = DatastoreClient(host=args.host)

    requests = client.replicator_put(generate_requests())
    for request in requests:
        key = request.data
        print("## PUT Response: key = " + key)
        print("## GET Request: key = " + key)
        value_response = client.get(key)
        print("## GET Response: value = " + value_response.data)

    print("\n@@@@@@@@@@@@@@Follower Replicator@@@@@@@@@@@@@@")
    client.replicator();

    requests = client.replicator_put(generate_requests_again())
    for request in requests:
        key = request.data
        print("## PUT Response: key = " + key)
        print("## GET Request: key = " + key)
        value_response = client.get(key)
        print("## GET Response: value = " + value_response.data)

    print("\n@@@@@@@@@@@@@@Follower Replicator@@@@@@@@@@@@@@")
    client.replicator();


if __name__ == "__main__":
    main()
