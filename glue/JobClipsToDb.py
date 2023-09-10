import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

args = getResolvedOptions(sys.argv,['JOB_NAME', 'DATA_SINK'])

#Initializing Glue and Spark Contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

s3_path = args['DATA_SINK']

try:
    glue_df = glueContext.create_dynamic_frame.from_options("s3", {'paths': [s3_path], 'recurse': True,"groupFiles": "inPartition"}, format="parquet").toDF()

    #DB Connection Url if not setup as catalog. This can also be setup in secrets.
    #For ex. I have taken oracle DB as my target Db
    connection_options = {"url": f"jdbc:oracle:thin:@//localhost:1521/mydb",
                                    "dbtable": "myschema.mytable", "user": f"mydbuser",
                                    "password": "qwer1234"}

    glueContext.write_dynamic_frame.from_options(frame=glue_df, connection_type='oracle',connection_options=connection_options)
except Exception as e:
    print(f"Job Failed with excetion : {str(e)}")

job.commit()

