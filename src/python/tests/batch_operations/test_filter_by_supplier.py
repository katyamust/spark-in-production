#from spark_utils.schemas import message_schema
import spark_utils.batch_operations as batch_operations 

from pyspark.sql.types import StructType, StructField, StringType, ArrayType, DecimalType, TimestampType, BooleanType
import pytest
from decimal import Decimal
from datetime import datetime

date_time_formatting_string = "%Y-%m-%dT%H:%M:%S%z"
default_obs_time = datetime.strptime(
    "2020-01-01T00:00:00+0000", date_time_formatting_string)


@pytest.fixture(scope="module")
def valid_message_sample(spark, valid_atomic_value_schema):
    structureData = [
        ("217", "23", [Decimal(12345), "kWH"], default_obs_time)]
    df = spark.createDataFrame(data=structureData, schema=message_schema)
    return df


def test_extractValidMessageAtomicValues(valid_message_sample):
    test_df = batch_operations.filter_by_supplier(valid_message_sample)
    assert len(test_df.columns) == 1
