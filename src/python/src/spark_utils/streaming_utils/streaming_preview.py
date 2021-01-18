from pyspark.sql.dataframe import DataFrame


def preview_stream(stream: DataFrame, await_seconds: int = 5):
    stream.printSchema()
    exec = stream \
        .writeStream \
        .foreachBatch(lambda df, i: df.show()) \
        .start()
    exec.awaitTermination(await_seconds)
    exec.stop()
