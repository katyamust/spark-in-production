from pyspark.sql.functions import col, from_json
from pyspark.sql import DataFrame
from spark_utils.schemas import message_schema


def event_hub_parse(raw_data: DataFrame):
    return raw_data \
        .select(from_json(col("body").cast("string"), message_schema).alias("message"),
                col("enqueuedTime")) \
        .select(col("message.*"),
                col("enqueuedTime").alias("EventHubEnqueueTime"))
