
## AI Engineering Tech Test
Firstly, thanks for considering me! As requested, here's the tech test of creating a Data Ingest, and then an API. There's a few things needed to get the code going, which is explained below.

### 1. Postgres Table Creation
The DB of choice I've used is Postgres, simply as I know it's used in small doses in AI Engineering, and wanted to keep my code as 'realistic as possible'. 

The below command can be run in the Postgres CLI to create the relevant schema and table in Postgres (I've used `sample_data` as a schema, and `aieng_tech_test` as the table, but these can be changed).

```
create table sample_data.aieng_tech_test
(
    id          serial
        constraint aieng_tech_test_pk
            primary key,
    timestamp   int not null,
    cpu_load    real not null,
    concurrency int not null
);

create unique index aieng_tech_test_id_uindex
    on sample_data.aieng_tech_test (id);

create unique index aieng_tech_test_timestamp_uindex
    on sample_data.aieng_tech_test (timestamp);
```
### 2. Python Dependency Installation
Both the API and Data Ingest are coded using Python, therefore to ensure all modules are installed for both files to run, please run in your Terminal (please ensure you've CD'd into the root directory of the code:
```
python -m pip -r requirements.txt
```
N.B. the version of Python this code has been created in is 3.9.13

### 3. Setting your Environment Variables
The code relies on the Postgres DB, however to make life easier, all of the DB config has been set as Vars.

To make life easier, I have put a blank .env file in the repo where you can set these values. (In real life, the vars would be stored in ConfigMaps and Secrets)

### 4. Running the code (and hopefully it works!)

Once all the above has been done, you should be able to run the code!

#### Data Ingest

Starting the Data Ingest can be done by CD'ing into data_ingest and running:

```
python ingest.py
```
The script will output if all is well, and if it's successfully ingested a record, it'll return the ID number of it onto stdout for you.

#### Data API

Starting the Data API relies on Flask, so you should be able to start it by CD'ing into data_api and running:

```
flask run
```

Where the URL and Port Number will be returned to you, for where you can query the API.

There are two routes available on the API:

- /api/metrics
- /healthz

If you do a GET request to `/api/metrics` it will simply return all results in a nice JSON format back to you (not ideal in the long-run if there's a lot of data, we could do some indexing/pagination to improve this if going into Production.)

To get the records between a specific timestamp, you can use parameters of `start` and `end` and set the relevant epoch date/time that you wish to see the data for (works for now, but going forward we know that users would probably not want both options, so we could improve the handling to only use start/end as independent paramaters).

If you do a GET request to `healthz`, you'll simply see a response (JSON encoded) of `Ping!`. This is to be used for checking the uptime of the application (Maybe in GCP Uptime Checks for future monitoring). If the app fails for whatever reason, this route would also stop, allowing for alerts to be raised.

### Final Thoughts & Improvements

1. Pagination & Number of Results to be setup, especially when the size of records in the DB grows.
2. Better Filter handling for start/end epoch, as some users will want to be able to query from just a start or end.
3. Improvements on the Data Ingest (which depends on how the data is presented at Ingest). In this example, the JSON array could likely have been done tidier, rather than just having 6 static objects setup.
4. OTel/APM integration, so we can see performance of the API, and detailed traces which can be alerted on for latency/errors and so forth. Also helps if this code is in a dynamic scaling environment (K8s) where pods have the ability to scale.
5. Re-factor to Go (apologies this is all in Python, I know it's not as slick as Go in terms of speed!)


