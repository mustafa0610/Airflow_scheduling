# Scheduling ETL Tasks with Apache Airflow

This project demonstrates a simple ETL (Extract, Transform, Load) pipeline using **Apache Airflow**. The pipeline reads a CSV file containing laptop product data, transforms the data to extract relevant columns (Company and Product), and loads the transformed data into a **PostgreSQL** database hosted in a **Docker** container.

## Key Steps:

1. **Extract**: Reads a local CSV file containing laptop pricing data.
2. **Transform**: Filters out unnecessary columns, keeping only the Company and Product information.
3. **Load**: Inserts the transformed data into a PostgreSQL database.

This pipeline is orchestrated using **Airflow**, leveraging **DAGs (Directed Acyclic Graphs)** for scheduling and managing tasks. Docker is used to run the PostgreSQL database, and Airflow's `PythonOperator` facilitates each step of the ETL process.

## Technologies Used:

- Apache Airflow
- PostgreSQL
- Docker
- Python

