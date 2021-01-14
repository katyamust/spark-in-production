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
from pyspark.sql import DataFrame
from pyspark.sql.functions import year, month, dayofmonth, \
    col


def store_data(batch_df: DataFrame, output_delta_lake_path):
    batch_df \
        .select(col("MarketEvaluationPoint_mRID"),
                col("Period_Point_ObservationTime").alias("ObservationTime"),
                col("Period_Point_Quantity").alias("Quantity"),
                col("CorrelationId"),
                col("MessageReference"),
                col("MarketDocument_mRID"),
                col("MarketDocument_CreatedDateTime").alias("CreatedDateTime"),
                col("MarketDocument_SenderMarketParticipant_mRID").alias("SenderMarketParticipant_mRID"),
                col("MarketDocument_ProcessType").alias("ProcessType"),
                col("MarketDocument_SenderMarketParticipant_Type").alias("SenderMarketParticipantMarketRole_Type"),
                col("TimeSeries_mRID"),
                col("MktActivityRecord_Status"),
                col("MarketEvaluationPointType"),
                col("Period_Point_Quality").alias("Quality"),

                year("Period_Point_ObservationTime").alias("year"),
                month("Period_Point_ObservationTime").alias("month"),
                dayofmonth("Period_Point_ObservationTime").alias("day")) \
        .repartition("year", "month", "day") \
        .write \
        .partitionBy("year", "month", "day") \
        .format("delta") \
        .mode("append") \
        .save(output_delta_lake_path)
