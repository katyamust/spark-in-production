# DevContainer Configuration

The [Visual Studio Code Remote - Containers extension](https://code.visualstudio.com/docs/remote/containers) lets you use a Docker container as a full-featured development environment. It allows you to open any folder or repository inside a container and take advantage of Visual Studio Code's full feature set. A devcontainer.json file in your project tells VS Code how to access (or create) a development container with a well-defined tool and runtime stack. This container can be used to run an application or to sandbox tools, libraries, or runtimes needed for working with a codebase. 

As Apache Spark is not that easy to install and configure properly, DevContainers provides a simple to use alternative to setup Spark Standalone and the corresponding development tools in minutes.

The dev environment inside the container can be spun up not only in VSCode locally, but also using [GitHub Codespaces](https://github.com/features/codespaces), which allows you to create cloud-based development environments accessible from VSCode or the web. That is especially desirable in Spark scenarios as it allows for hosting a heavy spark worker process out of the development machine.

Check the [documentation](https://code.visualstudio.com/docs/remote/create-dev-container) for a reference on available parameters and deployment options.

Table of content:

- [DevContainer Configuration](#devcontainer-configuration)
  - [Dockerfile](#dockerfile)
    - [Custom Spark/Hadoop version](#custom-sparkhadoop-version)
    - [Change python version and install additional packages](#change-python-version-and-install-additional-packages)
    - [Additional container configuration for Jupyter Stacks](#additional-container-configuration-for-jupyter-stacks)
  - [Spark configuration](#spark-configuration)

## Dockerfile

Dockerfile is the main place to configure all the required binary dependencies and installation scripts for a DevContainer.

In the specific case of Spark development environment prebuilt containers from [Jupyter Stack](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-pyspark-notebook) project can be an optimal solutions: they contain the latest configured single-node spark engine as well as all required dev tools. Check [jupyter/pyspark-notebook](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-pyspark-notebook) for Spark with PySpark interface and [jupyter/all-spark-notebook](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-all-spark-notebook) for a Spark engine with additional Scala and R support.

To use a prebuilt version put `FROM jupyter/pyspark-notebook:<VERSION_TAG>` at the top of the Dockerfile following by additional configuration steps (if any).

### Custom Spark/Hadoop version

Sometimes a specific Spark/Hadoop version configuration is needed to fit compatibility requirements. A modified [Dockerfile](./Dockerfile) based on [jupyter/pyspark-notebook](https://github.com/jupyter/docker-stacks/blob/master/pyspark-notebook/Dockerfile) was built that allows selection of which Spark and Hadoop versions to install and configure. Use the corresponding ARGs either directly in the Dockerfile or in the DevContainer `build.args` section to overwrite versions and checksums.

For available options check [Spark on Apache Mirror](https://apache-mirror.rbc.ru/pub/apache/spark/) and [Spark on Apache Archive](https://archive.apache.org/dist/spark/) for available Spark versions and [Hadoop Common on Apache Mirror](https://apache-mirror.rbc.ru/pub/apache/hadoop/common/) and [Hadoop Common on Apache Archive](https://archive.apache.org/dist/hadoop/common/) for Hadoop binaries. Make sure `spark-<VERSION>-bin-without-hadoop.tgz` and `hadoop-<VERSION>.tar.gz` are available in the corresponding version folders.

### Change python version and install additional packages

In order to change the prebuilt python uncomment the following code section at the end of the Dockerfile and specify the required value:

```Dockerfile
    # [Optional] Uncomment to install a different version of Python than the default
    # RUN conda install -y python=3.5 \
    #     && pip install --no-cache-dir pipx \
    #     && pipx reinstall-all
```

The next code section can be used to install additional conda and pip packages as well. Make sure that all additional packages has been added for development environment consistency. NOTE: Consider switching to the requirements.txt file in the root of the project or conda environment export.

```Dockerfile
RUN conda install --quiet --yes --satisfied-skip-solve \
    'pyarrow=2.0.*' 'rope=0.18.*' 'pytest=6.1.*' 'pylint=2.6.*' 'autopep8=1.5.*' 'configargparse=1.2.3' 'applicationinsights=0.11.9' && \
    pip --no-cache-dir install pyspelling azure-eventhub && \
    conda clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
```

You can always add other Dockerfile statements to fine tune container configuration.

### Additional container configuration for Jupyter Stacks

A few container settings are additionally specified in the .devcontainer.json file itself.

```json
{
    // ....

    "forwardPorts": [
        4041, 4042, 4043, 4044, 8888
    ],


    "containerEnv": {
        "GRANT_SUDO": "yes"
    },

    "overrideCommand": false,

    "containerUser": "root",

    "remoteUser": "jovyan"

    // ....
}
```

* `forwardPosts` automatically forwards 4 Spark UI ports as well as 8888 for jupyter notebooks.
* `containerEnv`, `overrideCommand`, `containerUser` and `remoteUser` are required to setup password-less sudo on the jovyan user. "jovyan" is the main user of the container intentionally built without any out-of-the-box root permissions. A special script at the entrypoint of the container (`overWriteCommand` makes sure it runs) check "GRANT_SUDO" environment variable and configures password-less sudo on jovyan user. `containerUser` and `remoteUser` guarantee that the entrypoint script runs with root permissions while VSCode still connects to jovyan session. Check [.devcontainer.json reference](https://code.visualstudio.com/docs/remote/devcontainerjson-reference) for more details.

## Spark configuration

Spark has its own set of parameters that can be specified during context creation. The most straightforward way is to set them directly in code like this:

```python
spark_conf = SparkConf(loadDefaults=True) \
    .set('fs.azure.account.key.{0}.dfs.core.windows.net'.format(args.storage_account_name),
         args.storage_account_key)
```

While this option is perfect for passwords and other secrets, it's far from optimal for common configuration. To reproduce DataBricks and other spark cluster's libraries management behavior as well as default configuration values, Spark Default Configuration can be used. [spark-defaults.conf](./spark-defaults.conf) file from `$SPARK_HOME/conf/` specifies the default configuration to be applied on every spark engine start. For convenience this file is located in the same .devcontainers folder and soft-linked to `$SPARK_HOME/conf` folder at container start. Make sure to restart Spark Session to apply updated values: normally restart of a debug or interactive session is enough.

```conf
# Default system properties included when running spark-submit.
# This is useful for setting default environmental settings.

# Example:
# spark.master                     spark://master:7077
# spark.eventLog.enabled           true
# spark.eventLog.dir               hdfs://namenode:8021/directory
# spark.serializer                 org.apache.spark.serializer.KryoSerializer
# spark.driver.memory               16g
# spark.executor.extraJavaOptions  -XX:+PrintGCDetails -Dkey=value -Dnumbers="one two three"

spark.jars.packages com.microsoft.azure:azure-eventhubs-spark_2.12:2.3.17,org.apache.hadoop:hadoop-azure:3.3.0,io.delta:delta-core_2.12:0.7.0
spark.sql.extensions io.delta.sql.DeltaSparkSessionExtension
spark.sql.catalog.spark_catalog org.apache.spark.sql.delta.catalog.DeltaCatalog
```

`spark.jars.packages` is of a special interest as it allows users to specify Maven coordinates to resolve and download automatically on startup. Check [Spark Configuration](http://spark.apache.org/docs/latest/configuration.html) section for other possible configuration parameters. For example, `io.delta:delta-core_2.12:0.7.0` is used here to enable Delta Lake functionality and storage sink for local development. Note, that `spark_defaults.conf` only accepts configuration lines starting with "spark.*", forcing users to add other values (like Azure Storage keys) in code through a `SparkConf` object (check the example above).
