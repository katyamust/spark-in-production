from pyspark.sql import DataFrame
from pyspark.sql.functions import col, lit


def filter_by_supplier(df: DataFrame, supplierId: str):
    supplier = str(supplierId)
    supplier_df = df.filter(col("SupplierId") == lit(supplier))
    return supplier_df
