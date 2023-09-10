from airflow import DAG
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from datetime import datetime, timedelta


def on_failure_callback(context):
    # Defining Failure callbacks to send email or notification to user

    subject = f"Airflow Task Failed: {context['task_instance'].task_id}"
    html_content = f"Task failed: {context['task_instance'].task_id}"
    print('youremail@example.com', subject, html_content) #Send email when required to user


#Setting Up default arguements for workflow. Keeping retires as 1, Retries per glue job has been modified to 3.
default_args = {
    'owner': 'tanuj',
    'start_date': datetime(2023, 9, 9),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


# Create the Airflow DAG with on_failure_callback
dag = DAG(
    'glue_job_sequence',
    description="This workflow runs glue jobs to calculate User interests on reels from reels like unlike and watched datasets.",
    default_args=default_args,
    schedule_interval='0 5 * * 1',  # Set the schedule interval to run Every Monday 5 am
    catchup=False, #Set to true if we wish to make up for missed DAG runs
    on_failure_callback=on_failure_callback,  # Specify the error callback
)

# Defining the Glue job 1 for clips interests calculation
glue_job_1 = GlueJobOperator(
    task_id='job-1',
    job_name='JobClips',
    aws_conn_id='aws_default',  # Your AWS connection ID
    region_name='us-east-1',  # Replace with your AWS region
    script_args={
        '--LIKED_PATH': 's3:/path/to/liked/data',
        '--UNLIKED_PATH': 's3:/path/to/unliked/data',
        '--WATCHED_PATH': 's3:/path/to/watched/data',
        '--DATA_SINK': 's3:/path/to/datasink',
    },  # Pass parameters as key-value pairs
    retries=3,  # Number of retries
    retry_delay=timedelta(minutes=5),  # retry after 5 minutes of failure
    dag=dag,
)

glue_job_2 = GlueJobOperator(
    task_id='job-2',
    job_name='JobClipsToDb',
    aws_conn_id='aws_default',  # Your AWS connection ID
    region_name='us-east-1',  # Replace with your AWS region
    script_args={
        '--DATA_SINK': 's3:/path/to/datasink', #Path to output file produced by job-1
    },  # Pass parameters as key-value pairs
    retries=3,  # Number of retries
    retry_delay=timedelta(minutes=5),  # Delay between retries
    dag=dag,
)


#Defining the workflow .  job-1 then job 2 will be executed.
glue_job_1 >> glue_job_2

if __name__ == "__main__":
    dag.cli()
