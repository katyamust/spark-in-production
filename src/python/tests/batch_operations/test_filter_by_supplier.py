import pytest
from decimal import Decimal
from datetime import datetime

from spark_utils.schemas import message_schema
import spark_utils.batch_operations as batch_operations


date_time_formatting_string = "%Y-%m-%dT%H:%M:%S%z"
default_obs_time = datetime.strptime(
    "2020-01-01T00:00:00+0000", date_time_formatting_string)


@pytest.fixture(scope="module")
def with_supplier23_df(spark):
    structureData = [("217", "23", [Decimal(12345), "kWH"], default_obs_time)]
    df = spark.createDataFrame(data=structureData, schema=message_schema)
    return df


def test_filter_by_supplier(with_supplier23_df):
    test_df = batch_operations.filter_by_supplier(with_supplier23_df, 23)
    assert test_df.toPandas()["SupplierId"][0] == "23"
