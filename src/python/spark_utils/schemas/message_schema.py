"""
Message schema for data Eneryg consumption Hub ingestion
"""

#import copy
from pyspark.sql.types import StructType, StringType, TimestampType, DecimalType

message_schema: StructType = StructType()\
    .add("MeterId", StringType(), False)\
    .add("SupplierId", StringType(), False)\
    .add("Measurement", StructType()\
        .add("Value", DecimalType(), False)\
        .add("Unit", StringType(), True),False)\
    .add("ObservationTime", TimestampType(), False)
   

    # eventhub_schema: StructType = copy.deepcopy(message_schema) \
    #     .add("EventHubEnqueueTime", TimestampType(), False)

    # @staticmethod
    # def get_instance():
    #     SchemaFactory.message_schema
    
    # @staticmethod
    # def get_parsed():
    #     return SchemaFactory.parsed_schema
