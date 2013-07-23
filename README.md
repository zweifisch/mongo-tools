# mongo tools

### mongo-info

list dbs and print storage size, number of documents etc. of each db

```sh
mongo-info dbs
```

print info of a single database

```sh
mongo-info db local
```

list all connections

```sh
mongo-info connections
```
more options see `mongo-info -h`

### mongo-profile

profile for 60 seconds, log queries that takes longer than 10 ms

```sh
mongo-profile 60 100
```
