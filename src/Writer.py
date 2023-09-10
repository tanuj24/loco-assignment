from src.Constants import Constants

class Writer:
    """Glue Dataframe writer class to write dataframe to s3 or local in desired format"""

    @staticmethod
    def write_parquet_to_local(df,file_name,partitions=1):
        df.coalesce(partitions).write.mode("overwrite").parquet(f"{Constants.DATA_SINK}/{file_name}")

    @staticmethod
    def write_csv_to_local(df,file_name,partitions=1):
        df.coalesce(partitions).write.mode("overwrite").csv(f"{Constants.DATA_SINK}/{file_name}")

    @staticmethod
    def write_json_to_local(df,file_name,partitions=1):
        df.coalesce(partitions).write.mode("overwrite").csv(f"{Constants.DATA_SINK}/{file_name}")
