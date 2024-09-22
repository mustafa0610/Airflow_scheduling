import os
import pandas as pd
import logging
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook

#define path to csv
LOCAL_CSV_PATH = '###' #add a path

#path to save the transformed csv(inside docker container)
TRANSFORMED_CSV_PATH = '###' #add a path

# DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 21),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Create the DAG
dag = DAG(
    'local_csv_to_postgres',
    default_args=default_args,
    description='Load and transform local CSV file and save to PostgreSQL',
    schedule_interval=None,
)

# Step 1: Read the csv and transform so only the Company and Product columns remain
def extract_transform():
    logging.info(f"Reading CSV from {LOCAL_CSV_PATH}")
    df = pd.read_csv(LOCAL_CSV_PATH)
    transformed_df = df[['Company', 'Product']]
    logging.info(f"Transformed data shape: {transformed_df.shape}")

    # save the transformed data to a new CSV
    logging.info(f"Saving transformed CSV to {TRANSFORMED_CSV_PATH}")
    transformed_df.to_csv(TRANSFORMED_CSV_PATH, index=False)

    return TRANSFORMED_CSV_PATH

# Step 2: Load the transformed data into the PostgreSQL database
def load_to_postgres():
    logging.info("Starting the load to PostgreSQL task")
    
    # Connect to PostgreSQL using the PostgresHook
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')

    # Log the connection parameters (access connection details directly from the hook)
    connection = pg_hook.get_connection('postgres_default')
    logging.info(f"Connecting to Postgres host: {connection.host}, database: {connection.schema}, user: {connection.login}")

    transformed_csv_path = TRANSFORMED_CSV_PATH

    logging.info(f"Reading transformed CSV from {transformed_csv_path}")
    df_transformed = pd.read_csv(transformed_csv_path)

    # Insert each row into PostgreSQL
    conn = pg_hook.get_conn()
    cursor = conn.cursor()

    for index, row in df_transformed.iterrows():
        logging.info(f"Inserting row {index} into the database")
        cursor.execute(
            """
            INSERT INTO laptop_products (company, product)
            VALUES (%s, %s)
            """, 
            (row['Company'], row['Product'])
        )
    
    # Commit the transaction
    conn.commit()
    cursor.close()
    conn.close()
    logging.info("Data successfully loaded into PostgreSQL")

# Task to extract and transform the data
extract_transform_task = PythonOperator(
    task_id='extract_transform',
    python_callable=extract_transform,
    dag=dag,
)

# Task to load the transformed data into PostgreSQL
load_to_postgres_task = PythonOperator(
    task_id='load_to_postgres',
    python_callable=load_to_postgres,
    dag=dag,
)

# Set the task order
extract_transform_task >> load_to_postgres_task
