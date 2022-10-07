import os
import psycopg2
from dotenv import load_dotenv
import random
import time
import datetime

load_dotenv()

# Set connection environment variables/secrets as vars for use in conn block.
DB = os.getenv('DB')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_PORT = os.getenv('DB_PORT')
DB_SCHEMA = os.getenv('DB_SCHEMA')
DB_TABLE = os.getenv('DB_TABLE')


def randomDataGenerator():
    # Create a JSON array with 6 different objects, with random cpu_load and concurrency values, and timestamps from now - 5 minutes.
    # Could find a nicer way of creating an array, rather than having to make 6 individual objects.
    payload = [
        {
            "timestamp": int(time.time()-300),
            "cpu_load": round(random.uniform(0, 100), 2),
            "concurrency": random.randint(0, 10000)
        },
        {
            "timestamp": int(time.time()-240),
            "cpu_load": round(random.uniform(0, 100), 2),
            "concurrency": random.randint(0, 10000)
        },
        {
            "timestamp": int(time.time()-180),
            "cpu_load": round(random.uniform(0, 100), 2),
            "concurrency": random.randint(0, 10000)
        },
        {
            "timestamp": int(time.time()-120),
            "cpu_load": round(random.uniform(0, 100), 2),
            "concurrency": random.randint(0, 10000)
        },
        {
            "timestamp": int(time.time()-60),
            "cpu_load": round(random.uniform(0, 100), 2),
            "concurrency": random.randint(0, 10000)
        },
        {
            "timestamp": int(time.time()),
            "cpu_load": round(random.uniform(0, 100), 2),
            "concurrency": random.randint(0, 10000)
        }
    ]
    return payload

# Whilst ingest.py is running, loop through the lines below continuously until closed.
while True:

    conn = psycopg2.connect(database=DB,
                            host=DB_HOST,
                            user=DB_USER,
                            password=DB_PASS,
                            port=DB_PORT)

    cursor = conn.cursor()

    print(f"Starting AIEng Tech Test Data Ingest at {datetime.datetime.now()}")
    # Looping through JSON array from the Random Data Generator function to get individual objects
    for x in randomDataGenerator():
        print(x)
        cursor = conn.cursor()
        sql = f'''INSERT INTO {DB_SCHEMA}.{DB_TABLE} (timestamp, cpu_load, concurrency) VALUES(%s, %s, %s) RETURNING id'''
        try:
            cursor.execute(sql, (x['timestamp'], x['cpu_load'], x['concurrency']))
            # Insert into Postgres, returning the ID number of the row just created in the DB
            conn.commit()
            rows = cursor.rowcount
            # Print to stdout the ID number of the record in Postgres post insertion
            print(f"Ingest into DB succeeded. {rows} inserted. ID number for this record is {cursor.fetchone()[0]}")
        except psycopg2.IntegrityError:
            print('Error - Integrity Error identified during ingest. Please debug.')
            continue
    # Once loop has finished, close cursor and connection to Postgres.
    cursor.close()
    conn.close()
    print(f"AIEng Tech Test Data Ingest completed at {datetime.datetime.now()}. Sleeping for 6 minutes.")
    #Sleep for 6 minutes, then start the loop again with freshly generated data.
    time.sleep(360)

