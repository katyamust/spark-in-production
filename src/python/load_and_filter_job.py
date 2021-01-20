"""
Demonstrates loading data stored in Data Lake to spark Dataframe,
filters and displays loaded Dataframe
In this example we emulate energy consumption metering scenario.
"""

# %%
import configargparse
from pathlib import Path

from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit

# %%
p = configargparse.ArgParser(prog='streaming_job.py',
                             description='Streaming Job Sample',
                              default_config_files=[Path(__file__).parent.joinpath(
                                 'configuration/run_args_streaming.conf').resolve().as_posix()],
                             formatter_class=configargparse.ArgumentDefaultsHelpFormatter)
p.add('--storage-account-name', type=str, required=True,
      help='Azure Storage account name (used for data output and checkpointing)')
p.add('--storage-account-key', type=str, required=True,
      help='Azure Storage key', env_var='STREAMING_STORAGE_KEY')
p.add('--storage-container-name', type=str, required=False, default='data',
      help='Azure Storage container name')
p.add('--output-path', type=str, required=False, default="delta/streaming-data/",
      help='Path to stream output storage location (deltalake) relative to container''s root')
p.add('--input-eh-connection-string', type=str, required=True,
      help='Input Event Hub connection string', env_var='STREAMING_INPUT_EH_CONNECTION_STRING')
p.add('--max-events-per-trigger', type=int, required=False, default=10000,
      help='Metering points to read per trrigger interval')
p.add('--trigger-interval', type=str, required=False, default='1 second',
      help='Trigger interval to generate streaming batches (format: N seconds)')
p.add('--streaming-checkpoint-path', type=str, required=False, default="checkpoints/streaming",
      help='Path to checkpoint folder for streaming')

args, unknown_args = p.parse_known_args()

if unknown_args:
    print("Unknown args:")
    _ = [print(arg) for arg in unknown_args]

# %% build spark context

spark_conf = SparkConf(loadDefaults=True) \
    .set('fs.azure.account.key.{0}.dfs.core.windows.net'.format(args.storage_account_name),
         args.storage_account_key)

spark = SparkSession\
    .builder\
    .config(conf=spark_conf)\
    .getOrCreate()

sc = spark.sparkContext
print("Spark Configuration:")
_ = [print(k + '=' + v) for k, v in sc.getConf().getAll()]


# %% Reading stored Dataframe from Delta lake

BASE_STORAGE_PATH = "abfss://{0}@{1}.dfs.core.windows.net/".format(
    args.storage_container_name, args.storage_account_name
)
print("Base storage url:", BASE_STORAGE_PATH)
output_delta_lake_path = BASE_STORAGE_PATH + args.output_path

print("Reading stored from delta lake...")

my_df = spark \
        .read \
        .format("delta") \
        .load(output_delta_lake_path)

print("Loaded Dataframe:")

my_df.show()

# %%

print("Filtered for SupplierId 19")

sp19_df = my_df.filter(col("SupplierId") == lit("19"))
sp19_df.show()

# %%
print("Job complete")