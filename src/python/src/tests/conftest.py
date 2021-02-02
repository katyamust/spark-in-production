"""
By having a conftest.py in this directory, we are able to add all packages
defined in the spark_utils directory in our tests.
"""

from datetime import datetime
from decimal import Decimal
import pytest
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import DecimalType, StructType, StringType, TimestampType


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
    """
    Return input message schema.
    It proved better to keep test schemas outside of the module to use them
    as a way to identify schema changes quickly.
    """
    schema = StructType() \
        .add("MeterId", StringType(), False)\
        .add("SupplierId", StringType(), False)\
        .add("Measurement", StructType()
             .add("Value", DecimalType(), False)
             .add("Unit", StringType(), True), False)\
        .add("ObservationTime", TimestampType(), False)
    return schema


# Create parsed data and master data Dataframes
@pytest.fixture(scope="session")
def message_factory(spark, message_schema):
    def factory(meterId=1,
                supplierId="A",
                measurementValue=1.0,
                measurementUnit="kWH",
                observationTime="2020-01-01T00:00:00+0000"
                ):

        default_obs_time = datetime.strptime(
            observationTime, "%Y-%m-%dT%H:%M:%S%z")
        structureData = [(meterId, supplierId, [Decimal(
            measurementValue), measurementUnit], default_obs_time)]

        return spark.createDataFrame(data=structureData, schema=message_schema)
    return factory
