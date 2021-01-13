from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType


class EventHubParser:

    @staticmethod
    def parse(raw_data: DataFrame, message_schema: StructType):
        return raw_data \
            .select(from_json(col("body").cast("string"),
                              message_schema,
                              options={"dateFormat": "yyyy-MM-dd'T'HH:mm:ss.SSSSSSS'Z'"}).alias("message")) \
            .select(col("message.*"))
