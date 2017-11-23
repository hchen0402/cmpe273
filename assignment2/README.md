### Assignment2 instruction of running

Create a Docker image using [this example](https://github.com/sithu/cmpe273-fall17/tree/master/docker).

* Create a Docker network so that each container can connect to the host under the fixed IP 192.168.0.1.

```sh
docker network create -d bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1 dockernet
```

* Run the server, client.

```sh
# Generate Stub for client and server
docker run -it --rm --name grpc-tools -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 -m grpc.tools.protoc -I. --python_out=. --grpc_python_out=. datastore.proto


# Server
docker run -p 3000:3000 -it --rm --name lab1-server -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 server.py

# Client
docker run -it --rm --name lab1-client -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 client.py 192.168.0.1
```

### Expected Output on Client

```sh
Client is connecting to Server at 192.168.0.1:3000...

## PUT Request: value = foo
## PUT Response: key = 6ab47f0373cd4283b31fe0ec33a8754b
## GET Request: key = 6ab47f0373cd4283b31fe0ec33a8754b
## GET Response: value = foo

## PUT Request: value = bar
## PUT Response: key = 8a9055417ad6414091894c5b5b4b5188
## GET Request: key = 8a9055417ad6414091894c5b5b4b5188
## GET Response: value = bar

## PUT Request: value = hello
## PUT Response: key = 00d05f72a3e849ba8f6896db8ba8d2bd
## GET Request: key = 00d05f72a3e849ba8f6896db8ba8d2bd
## GET Response: value = hello

## PUT Request: value = world
## PUT Response: key = 8c744e0794334b56885b4cbe2e2fa4c3
## GET Request: key = 8c744e0794334b56885b4cbe2e2fa4c3
## GET Response: value = world

@@@@@@@@@@@@@@Follower Replicator@@@@@@@@@@@@@@
{6ab47f0373cd4283b31fe0ec33a8754b : foo} has been stored in the follower's DB.
{8a9055417ad6414091894c5b5b4b5188 : bar} has been stored in the follower's DB.
{00d05f72a3e849ba8f6896db8ba8d2bd : hello} has been stored in the follower's DB.
{8c744e0794334b56885b4cbe2e2fa4c3 : world} has been stored in the follower's DB.

## PUT Request: value = This
## PUT Response: key = fc55907c91d6495ebe25a0a6cd043cbf
## GET Request: key = fc55907c91d6495ebe25a0a6cd043cbf
## GET Response: value = This

## PUT Request: value = is
## PUT Response: key = 58ca973b7f3440cf9265f14ea37f8442
## GET Request: key = 58ca973b7f3440cf9265f14ea37f8442
## GET Response: value = is

## PUT Request: value = cmpe273
## PUT Response: key = 538bb7f2bd2d4f73a329ffb4ba7c38f0
## GET Request: key = 538bb7f2bd2d4f73a329ffb4ba7c38f0
## GET Response: value = cmpe273

@@@@@@@@@@@@@@Follower Replicator@@@@@@@@@@@@@@
{fc55907c91d6495ebe25a0a6cd043cbf : This} has been stored in the follower's DB.
{58ca973b7f3440cf9265f14ea37f8442 : is} has been stored in the follower's DB.
{538bb7f2bd2d4f73a329ffb4ba7c38f0 : cmpe273} has been stored in the follower's DB.
```