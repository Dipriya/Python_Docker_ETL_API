from flask import Flask
import time
import pandas as pd
import psycopg2 as ps
from psycopg2 import OperationalError

app = Flask(__name__)

def create_conn():
    conn = None
    while not conn:
        try:
            conn = ps.connect(
                database='userdata',
                user='postgres',
                password='po$t@dm!n90',
                host='localhost',
                port='5432'
            )
        except OperationalError as e:
            print(e)
            time.sleep(5)
    cursor = conn.cursor
    return conn


#@app.route('/etl')
def etl():
    # Load CSV files
    # Process files to derive features
    # Upload processed data into a database
    #pass
    
    users_df = pd.read_csv(r"data/users.csv")
    experiments_df = pd.read_csv(r"data/user_experiments.csv")
    compounds_df = pd.read_csv(r"data/compounds.csv")


# 1. Total experiments a user ran
    total_experiments = experiments_df.groupby('\tuser_id').size().reset_index(name='total_experiments')
    #print(total_experiments)

# 2. Average experiments amount per user
    average_experiments = experiments_df.groupby('\tuser_id').size().mean()
    #print(average_experiments)

# 3. User's most commonly experimented compound
    common_compound = experiments_df.groupby('\tuser_id')['\texperiment_compound_ids'].apply(lambda x: x.str.split(';').explode().mode()[0])
    #print(common_compound)

    processed_data = pd.DataFrame({
        '\tuser_id': total_experiments['\tuser_id'],
        'total_experiments': total_experiments['total_experiments'],
        'average_experiments': average_experiments,
        'common_compound': common_compound
    })

    #print (processed_data)

    data = [
        (
            row['\tuser_id'],
            row['total_experiments'],
            row['average_experiments'],
            row['common_compound']
        )
        for _, row in processed_data.iterrows()
    ]

    #print(data)
   
    #conn = create_conn()
    
# Create a cursor object to execute SQL queries
    
    cursor = create_conn().cursor()

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS processed_data (
        user_id NUMERIC PRIMARY KEY,
        total_experiments NUMERIC,
        average_experiments NUMERIC,
        common_compound TEXT
    )
    '''
    cursor.execute(create_table_query)

    insert_query = '''
    INSERT INTO processed_data (\tuser_id, total_experiments, average_experiments, common_compound)
    VALUES (%s,%s,%s,%s) on conflict (\tuser_id) do nothing
    '''

    cursor.executemany(insert_query, data)
    create_conn().commit

    if cursor.rowcount == 0:
        print("Records were already inserted and duplicate records are not valid.")
    else:
        print(cursor.rowcount, "Records inserted successfully.")

# Close the cursor and connection
    if cursor is not None:
        cursor.close()

    if create_conn() is not None:
        create_conn().close()

        return 'Success'


# Your API that can be called to trigger your ETL process
@app.route('/trigger_etl')
def trigger_etl():
    # Trigger your ETL process here
    etl()
    return {"message": "ETL process started"}, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')