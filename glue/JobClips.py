import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

from src import Constants, Clips

args = getResolvedOptions(sys.argv,['JOB_NAME','LIKED_PATH','UNLIKED_PATH','WATCHED_PATH', 'DATA_SINK'])

#setting up path constants in case they are available as glue job parameters.
Constants = Constants()
Constants.LIKED_PATH = args['LIKED_PATH']
Constants.UNLIKED_PATH = args['UNLIKED_PATH']
Constants.WATCHED_PATH = args['WATCHED_PATH']
Constants.DATA_SINK = args['DATA_SINK']

#Initializing Glue and Spark Contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

print("Job Started : " , args['JOB_NAME'])

try:
    #running reels interests calculation
    watched_df = spark.read.json(Constants.WATCHED_PATH)
    liked_df = spark.read.json(Constants.LIKED_PATH)
    unliked_df = spark.read.json(Constants.UNLIKED_PATH)
    clip = Clips(watched_df, liked_df, unliked_df)
    clip.run()
    interests_df = clip.interests_df

    #save data to s3
    print(f"writing parquet of interests_data to {Constants.DATA_SINK}")
    glue_df = DynamicFrame.fromDF(interests_df, glueContext, "TRANSFORMED_DF")
    datasink = glueContext.write_dynamic_frame.from_options(frame = glue_df,
                                connection_type = "s3",
                                connection_options = {"path": Constants.DATA_SINK},
                                format = "parquet",
                                format_options = {"useGlueParquetWriter":True})
    print(f"writing parquet of interests_data to {Constants.DATA_SINK} complete")
except Exception as e:
    print(f"Job Failed with exception : {str(e)}")
job.commit()
