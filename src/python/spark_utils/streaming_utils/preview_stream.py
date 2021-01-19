from pyspark.sql import DataFrame


def preview_stream(df_stream: DataFrame, await_seconds: int = 5):
    df_stream.printSchema()
    exec = df_stream \
        .writeStream \
        .foreachBatch(lambda df, i: df.show()) \
        .start()
    exec.awaitTermination(await_seconds)
    exec.stop()