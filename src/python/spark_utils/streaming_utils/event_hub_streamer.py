import copy
from pyspark.sql.types import StructType, TimestampType
from pyspark.sql.functions import col, from_json
from pyspark.sql import DataFrame

from spark_utils.schemas import message_schema


class EventHubStreamer:

    @staticmethod
    def eventhub_schema() -> StructType:
        eh_schema = copy.deepcopy(message_schema) \
         .add("EventHubEnqueueTime", TimestampType(), False)
        return eh_schema

    @staticmethod
    def parse(raw_data: DataFrame, message_schema: StructType):
        return raw_data \
                .select(from_json(col("body").cast("string"),\
                                    message_schema,
                                    options={"dateFormat": "yyyy-MM-dd'T'HH:mm:ss.SSSSSSS'Z'"}).alias("message")) \
                .select(col("message.*"))

    @staticmethod
    def preview_stream(df_stream: DataFrame, await_seconds: int = 5):
        df_stream.printSchema()
        exec = df_stream \
            .writeStream \
            .foreachBatch(lambda df, i: df.show()) \
            .start()
        exec.awaitTermination(await_seconds)
        exec.stop()
