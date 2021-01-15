from pyspark.sql import DataFrame
from pyspark.sql.functions import col


"""
Utility stores streaming dataframe to Data Lake Gen 2
using Delta lake framework
"""
def store_data(batch_df: DataFrame, output_delta_lake_path):
    batch_df.select(col("MeterId"),
                    col("SupplierIdSupplierId"),
                    col("Measurement"),
                    col("ObservationTime")) \
              .write \
              .format("delta") \
              .mode("append") \
              .save(output_delta_lake_path)

#.repartition("year", "month", "day") \ 
# .partitionBy("year", "month", "day") \