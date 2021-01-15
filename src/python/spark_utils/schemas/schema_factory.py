"""
Message schema for data ingestion
"""

import copy
from pyspark.sql.types import StringType, StructType, StructField, \
    TimestampType, DecimalType
#from .schema_names import SchemaNames


# # See NOTE on usage
# def make_all_nullable(schema):
#     schema.nullable = True
#     if isinstance(schema, StructField):
#         make_all_nullable(schema.dataType)
#     if isinstance(schema, ArrayType):
#         make_all_nullable(schema.elementType)
#     if isinstance(schema, StructType):
#         for f in schema.fields:
#             make_all_nullable(f)


class SchemaFactory:

    message_body_schema: StructType = StructType()\
        .add("MeterId", StringType(), False)\
        .add("SupplierId", StringType(), False)\
        .add("Measurement", DecimalType(), False)\
        .add("ObservationTime", TimestampType(), False)

    #parsed_schema: StructType = copy.deepcopy(message_body_schema) \
    #    .add("EventHubEnqueueTime", TimestampType(), False)

    # NOTE: This is a workaround because for some unknown reason pyspark parsing from JSON
    #       (in event_hub_parser.py) causes all to be nullable regardless of the schema
    #make_all_nullable(parsed_schema)

    @staticmethod
    def get_instance():
        SchemaFactory.message_body_schema
    
    # def get_instance(schema_name: SchemaNames):
    #     if schema_name is SchemaNames.Parsed:
    #         return SchemaFactory.parsed_schema
    #     elif schema_name is SchemaNames.MessageBody:
    #         return SchemaFactory.message_body_schema
    #     else:
    #         return None
