import pytest
from UnitTestCases import UnitTestCases
from src.Clips import Clips
from pyspark.sql import SparkSession

test_cases = [UnitTestCases.test_liked_only_event,
            UnitTestCases.test_unliked_only_event,
            UnitTestCases.test_watched_only_event]

@pytest.fixture(scope="module")
def spark():
    spark = SparkSession.builder.appName("TestClips").getOrCreate()
    yield spark
    spark.stop()

@pytest.fixture(params=test_cases)
def test_data(request):
    return request.param


def test_run_clips(spark, test_data):
    watched_df = spark.createDataFrame(test_data['reel_watched_data'])
    liked_df = spark.createDataFrame(test_data['reel_liked_data'])
    unliked_df = spark.createDataFrame(test_data['reel_unliked_data'])
    expected_result = test_data['expected_result'][0]

    cl = Clips(watched_df, liked_df, unliked_df)
    cl.run()
    result_df = cl.interests_df.rdd.map(lambda x : x.asDict(True)).take(1)[0]
    assert result_df == expected_result

