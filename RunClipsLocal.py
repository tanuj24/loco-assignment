from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import Window
from src.Clips import Clips
from src.Constants import Constants
from src.Writer import Writer

if __name__=="__main__":
    spark = SparkSession.builder.config("spark.master", "local[*]").appName("loco").getOrCreate()

    liked_df = spark.read.json(Constants.LIKED_PATH)
    unliked_df = spark.read.json(Constants.UNLIKED_PATH)
    watched_df = spark.read.json(Constants.WATCHED_PATH)

    cl = Clips(watched_df, liked_df, unliked_df)
    cl.run()
    interests_df = cl.interests_df

    interests_df.show(truncate=False)
    Writer.write_parquet_to_local(interests_df, 'interests_results')
