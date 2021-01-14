from pyspark.sql import DataFrame
from pyspark.sql.functions import col

def store_data(batch_df: DataFrame, output_delta_lake_path):
    batch_df \
        .select(col("MeterId"), \
                col("SupplierIdSupplierId"), \
                col("Measurement"), \
                col("ObservationTime")) \
      #  .repartition("year", "month", "day") \
        .write \
      #  .partitionBy("year", "month", "day") \
        .format("delta") \
        .mode("append") \
        .save(output_delta_lake_path)
