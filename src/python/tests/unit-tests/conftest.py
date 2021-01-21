"""
By having a conftest.py in this directory, we are able to add all packages
defined in the streaming_package directory in our tests.
"""

import pytest
from pyspark import SparkConf
from pyspark.sql import SparkSession, DataFrame
import pandas as pd
import time
from pyspark.sql.types import StructType, IntegerType, StringType


# Create Spark Conf/Session
@pytest.fixture(scope="session")
def spark():
    spark_conf = SparkConf(loadDefaults=True) \
        .set("spark.sql.session.timeZone", "UTC")
    return SparkSession \
        .builder \
        .config(conf=spark_conf) \
        .getOrCreate()


# Schema of sample message data
@pytest.fixture(scope="session")
def message_schema():
    schema = StructType() \
        .add("ID", IntegerType()) \
        .add("Region", StringType())
    return schema


# Create parsed data and master data Dataframes
@pytest.fixture(scope="session")
def message_factory(spark, message_schema):
    def factory(id=1,
                region="A"):
        pandas_df = pd.DataFrame({
            "ID": [id],
            "Region": [region]})
        return spark.createDataFrame(pandas_df, schema=message_schema)
    return factory