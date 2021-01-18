"""
Message schema for Data Energy Consumption Hub ingestion
"""
from pyspark.sql.types import StructType, StringType, TimestampType, DecimalType


message_schema: StructType = StructType()\
    .add("MeterId", StringType(), False)\
    .add("SupplierId", StringType(), False)\
    .add("Measurement", StructType()
        .add("Value", DecimalType(), False)
        .add("Unit", StringType(), True),False)\
    .add("ObservationTime", TimestampType(), False)

