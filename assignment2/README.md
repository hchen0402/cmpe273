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
## PUT Response: key = ae92be85e7ff4351866f05bfc83598bb
## GET Request: key = ae92be85e7ff4351866f05bfc83598bb
## GET Response: value = foo

## PUT Request: value = bar
## PUT Response: key = e5e2b96aede84c05b30de814684d5210
## GET Request: key = e5e2b96aede84c05b30de814684d5210
## GET Response: value = bar

## PUT Request: value = hello
## PUT Response: key = 2a5a4dadaa834340a94bbc897ac0c7f0
## GET Request: key = 2a5a4dadaa834340a94bbc897ac0c7f0
## GET Response: value = hello

## PUT Request: value = world
## PUT Response: key = 576f730f19a240b4a630e4a1056af556
## GET Request: key = 576f730f19a240b4a630e4a1056af556
## GET Response: value = world

########Follower Replicator########
{ae92be85e7ff4351866f05bfc83598bb : foo} has been stored in the follower's DB.
{e5e2b96aede84c05b30de814684d5210 : bar} has been stored in the follower's DB.
{2a5a4dadaa834340a94bbc897ac0c7f0 : hello} has been stored in the follower's DB.
{576f730f19a240b4a630e4a1056af556 : world} has been stored in the follower's DB.

## PUT Request: value = This
## PUT Response: key = 58bb358d3d1e49a594f632c517ee172e
## GET Request: key = 58bb358d3d1e49a594f632c517ee172e
## GET Response: value = This

## PUT Request: value = is
## PUT Response: key = b95edb9c4a664e408f771be65d20f5b2
## GET Request: key = b95edb9c4a664e408f771be65d20f5b2
## GET Response: value = is

## PUT Request: value = cmpe273
## PUT Response: key = bfe80fd0b427454aabd8b3b024e31225
## GET Request: key = bfe80fd0b427454aabd8b3b024e31225
## GET Response: value = cmpe273

########Follower Replicator########
{58bb358d3d1e49a594f632c517ee172e : This} has been stored in the follower's DB.
{b95edb9c4a664e408f771be65d20f5b2 : is} has been stored in the follower's DB.
{bfe80fd0b427454aabd8b3b024e31225 : cmpe273} has been stored in the follower's DB.
```