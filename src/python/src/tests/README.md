## Unit Testing

Unit tests utilize a full-featured Spark context available though the [DevContainer](/.devcontainer/README.md) to simulate test workloads and assert the results. Pyhton unit-testing framework [`pytest`](https://docs.pytest.org/en/latest/) is used on top as the main archestration engine.

## Testing and Fixtures

In order to increase code reuse throughout testing, this sample relies on [`pytest` fixtures](https://realpython.com/pytest-python-testing/#fixtures-managing-state-and-dependencies), which allows reusing functions, objects, etc. across tests in the same file, as well as across many or all files in the broader test suite.
[Scopes](https://pythontesting.net/framework/pytest/pytest-session-scoped-fixtures/) can be applied to each fixture to determine how often the fixture creation should run.
For instance, when constructing the fixture shown below creating a Spark Session (which sometimes takes time to initialize), you can give it a "session" level scope, ensuring its re-use for all test cases that request the fixture during the run of the test suite.

```python
# Create Spark Conf/Session to be shared
@pytest.fixture(scope="session")
def spark():
    spark_conf = SparkConf(loadDefaults=True) \
        .set("spark.sql.session.timeZone", "UTC")
    return SparkSession \
        .builder \
        .config(conf=spark_conf) \
        .getOrCreate()

```

In order to share fixtures across tests and even test files (such as the Spark session, schemas, etc.), [`conftest.py` file](https://stackoverflow.com/questions/34466027/in-pytest-what-is-the-use-of-conftest-py-files#:~:text=External%20plugin%20loading%3A%20conftest.py%20is%20used%20to%20import,modules%20which%20might%20be%20needed%20in%20your%20tests.) can be used at the root of the testing directory.
Any fixtures defined in the root `conftest.py` files could also be overwritten in the test files themselves as well as in other closer `conftest.py` files throughout the nested test folder structure.

### Data Factories

Since most of the tests needs similar mock data in order to test the modules, the advantage of fixtures is utilized to create sharable data factories (like the one shown below) that would create PySpark DataFrames containing configurable data.
This process provides a central place for a lot of the mock data creation shared throughout the tests, making it very quick to make changes.
Tests can call these factory methods with optional inputs in order to specify column values and even interact with the Spark session at all.

```python
@pytest.fixture(scope="session")
def mock_data_factory(spark, data_schema):
    def factory(field1_value="1", field2_value="2"):
        pandas_df = pd.DataFrame({
            "field1": [field1_value],
            "field2": [field2_value],
            ...
        })
        return spark.createDataFrame(pandas_df, schema=data_schema)
    return factory

```

Since these factories were defined in the root `conftest.py`, we could use them across all tests and quickly make any necessary changes whenever the schemas changed.

### Parametrization

`pytest` also has a concept of [parametrized tests](https://realpython.com/pytest-python-testing/#parametrization-combining-tests).
By parametrizing the inputs to tests, anyone can feed inputs to the factories to create the specific DataFrames needed to test edge cases without rewriting a similar test many times.
Since an `id` is provided for each parameter set, it is easy to see which parameter sets cause test successes/failures.

```python
@pytest.mark.parametrize("field1, field2, expected",
    [
        pytest.param(1, 2, 3, id="If field1 is 1 and field2 is 2, result column should be 3"),
        pytest.param(3, 4, 3, id="If field1 is 3 and field2 is 4, result column should be 7"),
        ...
    ],
)
def test_function_a(field1, field2, expected, mock_data_factory):
    # Create DataFrame
    data = mock_data_factory(field1_value=field1, field2_value=field2)
    # Call function on the DataFrame
    result = function_a(data)
    # Make assertion on resultant DataFraMe
    assert result.first()["result"] == expected
```

### `pandas`

While native PySpark can be used to both create and make assertions on DataFrames, `pandas` can give a better alternative as it was often provides easier and more developer friendly interface.
Switching back and forth between `pandas` and PySpark DataFrames are also quite simple.

## Putting it all together

The above-discussed features of `pytest`, `pandas`, and PySpark provide a way to neatly structure tests following the AAA (Arrange-Act-Assert) testing pattern.

- Arrange: Data that should be shared across multiple tests can be defined in a fixture, either at the `conftest.py` level (if being shared across multiple test files - for us, this included the Spark session, mock data factories, etc.) or within a specific test file (ex. mock DataFrames, etc.).
- Act: To use the fixtures defined in the previous step, either directly pass in the fixtures as arguments into each test, or perform some action on these lower-level fixtures in another fixture that could then be reused across tests.
Each test can run the modularized PySpark function against the specified input data for the scenario being tested.
- Assert: Having followed all the above steps, the actual assertion portion ends up being clear and easy to implement.
In some cases, an inline assertion is sufficient, while in others, a helper function doing more in depth checks on output DataFrame rows is necessary.
As discussed above, `pandas` also helps in simplifying the process of asserting on a single row.

## Using This Sample

This code sample shows how to use pytest to create factory fixtures used to test modularized spark functions.
To run this code sample, you can open this folder in the [dev container](../../../../README.md), and then run `pytest` from the root level of the folder from the command line.
Test Explorer extensions, preinstalled the container, also allows run and debug tests inline as well.
The SparkSession and some other useful test fixtures (message factory and message schema) are defined in the testing root level `conftest.py`.
