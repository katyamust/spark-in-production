# Developing and running spark in production

This repo demonstrates how to set up local development environment for work with spark engine using dev containers and deploy spark code to production Spark cluster in Azure Databricks. Originally, this code base was created to improve production-ready spark development experience with familiar tools, like IntelliSense, refactoring, debugging and tests, and then extended to allow interactive experimentation as well as production deployment and integration testing.

Repo is based on a sample that reads data from Azure Event Hubs, processes the incoming messages and saves the result to Azure Data Lake. Local development experience is powered by a local spark instance installed in a DevContainer, while DevOps pipelines target GitHub Actions.

For more details and configuration options, check the corresponding folders:

* [Python development experience](./src/python/src)
* [Local environment: DevContainer](./.devcontainer)
* Unit Testing for [python](./src/python/src/tests) and [scala](./src/scala/src/test/scala)
* [CI/CD and Integration Tests](./.github/workflows)

## Getting started

### Prerequisites

* [Visual Studio Code](https://code.visualstudio.com/) with [Visual Studio Code Remote - Containers extension](https://code.visualstudio.com/docs/remote/containers)
* [Docker Desktop](https://www.docker.com/products/docker-desktop)
* Azure Subscription or try [Free Trial](https://azure.microsoft.com/en-us/free/)

Alternatively you can host the development environment in the cloud with [GitHub Codespaces](https://github.com/features/codespaces).

### Deploy required Azure resources

This sample depends on [Azure Event Hubs](https://azure.microsoft.com/en-us/services/event-hubs/) and [Azure Data Lake Storage](https://azure.microsoft.com/en-us/services/storage/data-lake-storage/) as interim storage locations. Data generator pushes sample messages to the EventHub, that then processed by local development environment and the results with the corresponding checkpointing information are stored to Azure Storage. Follow the guides below to create the resources manually:

* [Quickstart: Create an event hub using Azure portal](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-create)
* [Create a storage account](https://docs.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal): make sure to set "Hierarchical namespace" to "Enabled".

### Configure the sample

Use the [configuration files](./src/python/src/configuration) to set connection information for the storage account and the event hub. Make sure to specify event hub's connection strings with at least "SEND" claim in [run_args_data_generator.conf.sample](./src/python/src/configuration/run_args_data_generator.conf.sample) and "LISTEN" claim in [run_args_streaming.conf.sample](./src/python/src/configuration/run_args_streaming.conf.sample). At the end, remove `.sample` extension from the configuration files to make them visible to the scripts.

### Start local development environment

This sample uses DevContainers to quickly startup an environment with Spark and other binary prerequisites installed. Open the repository root folder in VSCode and accept the invitation to reopen the folder in devcontainer. If not prompted, follow the [documentation](https://code.visualstudio.com/docs/remote/containers) for a detailed guide. Note, that you can start the container remotely using GitHub Codespaces service, check [here](https://docs.github.com/en/github/developing-online-with-codespaces/using-codespaces-in-visual-studio-code).

The first container build usually takes about 5-10 minutes as it installs Spark and its dependencies, next runs will reuse the container image, making the start process almost instantaneous. Check the [.devcontainer](./.devcontainer) for a detailed description of configuration options and the overall spark container design.

#### Note on GitHub integration

This container automatically installs [GitHub Codespaces](https://marketplace.visualstudio.com/items?itemName=GitHub.codespaces) and [GitHub Pull Requests and Issues](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github) extensions to simplify usage of GitHub Codespaces as well as allow issues and pull requests management from the VSCode instance.

Another important issue is git credentials management. If you use GitHub Codespaces or has originally cloned the repo with Git for Windows, you should be all set and VSCode will automatically propagate you credentials with username and email to the container. Otherwise, consult [Sharing Git credentials with your container](https://code.visualstudio.com/docs/remote/containers#_sharing-git-credentials-with-your-container) for more details.

### Generate sample data

This sample provides a data generator to be used with the main processing script. Once the container is running, navigate to [data-generator.ipynb](./src/python/src/data-generator.ipynb) and execute all cells (select the cell and click `Shift+Enter`). The code inside the notebook will initiate a local spark instance and start sending data to the Event Hub.

Check the interactive section of the [README](./src/python/src/README.md#experimentation_and_interactive_development) for mode details on jupyter-like development.

### Run the streaming job

Once the generator has started, switch to [streaming_job.py](./src/python/src/streamin_job.py) to start the streaming process locally. You can either start it through the local debugging session or the interactive environment by executing in-code cells individually. Check the [README](./src/python/src/README.md) for more information on dev experience.

### Unit tests

To run python unit tests, go to the [python src](./src/python/srs/) and execute `pytest tests`. The tests themself utilize the DevContainer to access the running Spark engine during the execution and manage to keep performance through the extensive use of fixtures. Check the corresponding [README](./src/python/src/tests/README.md) for more details.
