# mongo tools

install via pip

```sh
pip install mongo-tools
```

### mongo-info

list dbs and print storage size, number of documents etc. of each db

```sh
mongo-info dbs
```

example output

```
db_name
                  ns         storageSize                size      totalIndexSize               count
               links              13.4 M              10.0 M             503.0 K               8.9 k
      system.indexes               1.3 M             504.0                 0.0                 5.0  
             archive               3.7 M               3.3 M               2.4 M               6.8 k
            fs.files             168.0 K              62.2 K              39.9 K             264.0  
           fs.chunks             218.8 M             173.4 M              87.8 K             751.0  
            sessions             680.0 K              79.7 K              47.9 K             340.0  
```

print info of a single database

```sh
mongo-info db local
```

list all connections

```sh
mongo-info connections
```

example output:

```
           ip          counts
    127.0.0.1              41
      0.0.0.0               2
```

more options see `mongo-info -h`

### mongo-profile

profile for 60 seconds, log queries that takes longer than 100 ms

```sh
mongo-profile start db_name 100 60
```

more options see `mongo-profile -h`
