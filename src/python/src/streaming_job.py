"""
Data ingestion stream
In this example we emulate energy consumption metering scenario.
"""

# %%
import json
import configargparse

from pathlib import Path

from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame

from spark_utils.streaming_utils import event_hub_parse, preview_stream
import spark_utils.batch_operations as batch_operations

# %% set up agruments

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

# %% configure event hub reading

input_eh_starting_position = {
    "offset": "-1",         # - 1 : starting from beginning of stream
    "seqNo": -1,            # not in use
    "enqueuedTime": None,   # not in use
    "isInclusive": True
}
input_eh_connection_string = args.input_eh_connection_string
input_eh_conf = {
    # Version 2.3.15 and up requires encryption
    'eventhubs.connectionString': \
    sc._jvm.org.apache.spark.eventhubs.EventHubsUtils.encrypt(
        input_eh_connection_string),
    'eventhubs.startingPosition': json.dumps(input_eh_starting_position),
    'maxEventsPerTrigger': args.max_events_per_trigger,
}

print("Input event hub config:", input_eh_conf)

# %% Read from Event Hub

raw_data = spark \
    .readStream \
    .format("eventhubs") \
    .options(**input_eh_conf) \
    .option("inferSchema", True)\
    .load()

print("Input stream schema:")
raw_data.printSchema()

# %% parse event hub message
eh_data = event_hub_parse(raw_data)

print("Parsed stream schema:")
eh_data.printSchema()

print("Stream preview:")
preview_stream(eh_data, await_seconds=5)

# %% store data to data lake

BASE_STORAGE_PATH = "abfss://{0}@{1}.dfs.core.windows.net/".format(
    args.storage_container_name, args.storage_account_name
)

print("Base storage url:", BASE_STORAGE_PATH)

output_delta_lake_path = BASE_STORAGE_PATH + args.output_path
checkpoint_path = BASE_STORAGE_PATH + args.streaming_checkpoint_path

# checkpointLocation is used to support failure (or intentional shut-down)
# recovery with a exactly-once semantic. See more on
# https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#fault-tolerance-semantics.


def __store_data_frame(batch_df: DataFrame, _: int):
    try:
        # Cache the batch in order to avoid the risk of recalculation in each write operation
        # Cache the batch in order to avoid the risk
        # of recalculation in each write operation
        batch_df = batch_df.persist()

        # Make valid time series points available to aggregations (by storing in Delta lake)
        # Make valid time series points available to post processing
        # (by storing in Delta lake)
        batch_operations.store_data(batch_df, output_delta_lake_path)

        # <other operations may go here>

        batch_df = batch_df.unpersist()

    except Exception as err:
        raise err


print("Writing stream to delta lake...")
out_stream = eh_data \
    .writeStream \
    .option("checkpointLocation", checkpoint_path) \
    .trigger(processingTime="1 second") \
    .foreachBatch(__store_data_frame)


execution = out_stream.start()
execution.awaitTermination(30)
execution.stop()

print("Job complete.")
# %%
