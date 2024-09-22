# Airflow_scheduling
Scheduling ETL tasks with airflow

This project demonstrates a simple ETL (Extract, Transform, Load) pipeline using Apache Airflow. The pipeline reads a CSV file containing laptop product data, transforms the data to extract relevant columns (Company and Product), and loads the transformed data into a PostgreSQL database hosted in a Docker container.

Key Steps:
Extract: Reads a local CSV file containing laptop pricing data.
Transform: Filters out the unnecessary columns, keeping only the Company and Product information.
Load: Inserts the transformed data into a PostgreSQL database.
This pipeline is orchestrated using Airflow, leveraging DAGs (Directed Acyclic Graphs) for scheduling and managing tasks. Docker is used to run the PostgreSQL database, and Airflow's PythonOperator facilitates each step of the ETL process.
