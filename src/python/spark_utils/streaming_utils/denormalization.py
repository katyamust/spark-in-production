
from pyspark.sql.functions import explode, col
from pyspark.sql import DataFrame

from spark_utils.dataframelib import flatten_df


def denormalize_parsed_data(parsed_data: DataFrame) -> DataFrame:
    flattened_parsed_data = flatten_df(parsed_data)
    exploded_data = flattened_parsed_data.select(col("*"), explode(col("Period_Points")).alias("Period_Point")) \
                                         .drop("Period_Points")
    denormalized_parsed_data = flatten_df(exploded_data)
    print("denormalized_parsed_data:")
    print(denormalized_parsed_data)
    return denormalized_parsed_data
