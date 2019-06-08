# mongodb-simple-backup
This program dumps all databases of mongodb using [mongodump](https://docs.mongodb.com/manual/reference/program/mongodump/) command, and upload them to [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/).

[![TravisCI Status](https://travis-ci.org/RoboticBase/mongodb-simple-backup.svg?branch=master)](https://travis-ci.org/RoboticBase/mongodb-simple-backup)
[![Docker image size](https://img.shields.io/microbadger/image-size/roboticbase/mongodb-simple-backup.svg)](https://hub.docker.com/r/roboticbase/mongodb-simple-backup/)

## Requirement

**python 3.6 or higer**

## Environment Variables
This application accepts the Environment Variables like below:

|Environment Variable|Summary|Mandatory|Default|
|:--|:--|:--|:--|
|`MONGODB_ENDPOINT`|mongodb host|yes||
|`STORAGE_ACCOUNT`|the storage account of azure storage|yes||
|`ACCOUNT_KEY`|account key of the storage acount|yes||
|`STORAGE_CONTAINER`|storage container name of azure blob storage|yes||
|`LOG_LEVEL`|log level(DEBUG, INFO, WARNING, ERRRO, CRITICAL)|no|`INFO`|
|`TIMEZONE`|timezone used when naming dump file|no|`Asia/Tokyo`|
|`DUMPFILE_PREFIX`|dumpfile prefix|no|`mongodb_`|
|`STORE_OPLOG`|if True, oplog will be backed up|no|`False`|

## how to set `MONGODB_ENDPOINT`
###  non cluster
When you use a single mongodb, you have to set the `MONGODB_ENDPOINT` as `<hostname>:<port>` like below:

```
mongodb:27017
```

### cluster
When you use mongodb cluster, you have to set the `MONGODB_ENDPOINT` as `<replSet>/<hostname1>:<port1>,<hostname2>:<port2>,...` like below:

```
rs0/mongodb-0.mongodb:27017,mongodb-1.mongodb:27017,mongodb-2.mongodb:27017
```

## Run as Docker container

1. Pull container [roboticbase/mongodb-simple-backup](https://hub.docker.com/r/roboticbase/mongodb-simple-backup/) from DockerHub.

    ```bash
    $ docker pull roboticbase/mongodb-simple-backup:latest
    ```
1. Run Container.
    * Set environment variables and start container

    ```bash
    $ export MONGODB_ENDPOINT="mongodb:27017"
    $ export STORAGE_ACCOUNT="mystrageaccount"
    $ export ACCOUNT_KEY="myaccountkey"
    $ export STORAGE_CONTAINER="mongodumpcontainer"
    $ docker run -it -p 3000:3000 roboticbase/fiware-cmd-proxy
    $ docker run -it -e MONGODB_ENDPOINT -e STORAGE_ACCOUNT -e ACCOUNT_KEY -e STORAGE_CONTAINER roboticbase/mongodb-simple-backup:latest
    ```

## License

[Apache License 2.0](/LICENSE)

## Copyright
Copyright (c) 2019 TIS Inc.
