# Copyright 2020 Energinet DataHub A/S
#
# Licensed under the Apache License, Version 2.0 (the "License2");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import copy
from pyspark.sql.types import StringType, StructType, StructField, \
    TimestampType, DecimalType, ArrayType
from .schema_names import SchemaNames


# See NOTE on usage
def make_all_nullable(schema):
    schema.nullable = True
    if isinstance(schema, StructField):
        make_all_nullable(schema.dataType)
    if isinstance(schema, ArrayType):
        make_all_nullable(schema.elementType)
    if isinstance(schema, StructType):
        for f in schema.fields:
            make_all_nullable(f)


class SchemaFactory:

    message_body_schema: StructType = StructType() \
        .add("TimeSeries_mRID", StringType(), False) \
        .add("MessageReference", StringType(), False) \
        .add("MarketDocument", StructType()
             .add("mRID", StringType(), False)
             .add("Type", StringType(), False)
             .add("CreatedDateTime", TimestampType(), False)
             .add("SenderMarketParticipant", StructType()
                  .add("mRID", StringType(), False)
                  .add("Type", StringType(), False), False)
             .add("RecipientMarketParticipant", StructType()
                  .add("mRID", StringType(), False)
                  .add("Type", StringType(), True), False)
             .add("ProcessType", StringType(), False)
             .add("MarketServiceCategory_Kind", StringType(), False), False) \
        .add("MktActivityRecord_Status", StringType(), False) \
        .add("Product", StringType(), False) \
        .add("QuantityMeasurementUnit_Name", StringType(), False) \
        .add("MarketEvaluationPointType", StringType(), False) \
        .add("SettlementMethod", StringType(), True) \
        .add("MarketEvaluationPoint_mRID", StringType(), False) \
        .add("CorrelationId", StringType(), False) \
        .add("Period", StructType()
             .add("Resolution", StringType(), False)
             .add("TimeInterval_Start", TimestampType(), False)
             .add("TimeInterval_End", TimestampType(), False)
             .add("Points", ArrayType(StructType()
                                      .add("Quantity", DecimalType(), False)
                                      .add("Quality", StringType(), False)
                                      .add("ObservationTime", TimestampType(), False), True), False), False)

    parsed_schema: StructType = copy.deepcopy(message_body_schema) \
        .add("EventHubEnqueueTime", TimestampType(), False)
    # NOTE: This is a workaround because for some unknown reason pyspark parsing from JSON
    #       (in event_hub_parser.py) causes all to be nullable regardless of the schema
    make_all_nullable(parsed_schema)

    @staticmethod
    def get_instance(schema_name: SchemaNames):
        if schema_name is SchemaNames.Parsed:
            return SchemaFactory.parsed_schema
        elif schema_name is SchemaNames.MessageBody:
            return SchemaFactory.message_body_schema
        else:
            return None
