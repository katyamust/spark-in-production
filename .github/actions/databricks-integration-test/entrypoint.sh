#!/bin/bash

export SPARK_DIST_CLASSPATH=$(hadoop classpath)

echo "========= ENV INFO ==============="
echo "THE USER IS: $(whoami)"
cat $SPARK_HOME/conf/spark-defaults.conf
echo "=================================="

cd ./tests/integration-tests/
python streaming-test.py $1 $2 $3 $4 $5
