from pyspark.sql import DataFrame
from pyspark.sql.functions import col


def store_data(batch_df: DataFrame, output_delta_lake_path):
    """
    Utility stores streaming dataframe to Data Lake Gen 2
    using Delta lake framework
    """
    batch_df.select(col("MeterId"),
                    col("SupplierId"),
                    col("Measurement"),
                    col("ObservationTime")) \
            .repartition("SupplierId") \
            .write \
            .partitionBy("SupplierId") \
            .format("delta") \
            .mode("append") \
            .save(output_delta_lake_path)
