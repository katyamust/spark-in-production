import pytest
from spark_utils.batch_operations import filter_by_supplier


@pytest.fixture(scope="module")
def result_schema(message_schema):
    """
    The expected schema of result data after calculation
    """
    return message_schema


@pytest.fixture(scope="module")
def positive_result_df(message_factory):
    """
    Fixture to store the result of the case when supplier is available,
    since it is used across multiple tests
    """
    df = message_factory(supplierId="Sup1")

    return filter_by_supplier(df, "Sup1")


def test_filter_by_supplier_keeps_data_for_requested_supplier(positive_result_df):

    assert positive_result_df.count() == 1


def test_filter_data_schema_is_preserved(positive_result_df, result_schema):

    assert positive_result_df.schema == result_schema


def test_filter_by_supplier_drops_other_suppliers(message_factory):
    df = message_factory(supplierId="Sup1")

    res = filter_by_supplier(df, "Sup2")

    assert res.count() == 0

@pytest.mark.parametrize("supplierId, expected",
    [
        pytest.param('-1', '-1', id="Keeps supplier -1"),
        pytest.param('0', '0', id="Keeps supplier 0")
    ]
)
def test_filter_by_supplier_keeps_supplierid(message_factory, supplierId, expected):
    df = message_factory(supplierId=supplierId)

    test_df = filter_by_supplier(df, supplierId)

    assert test_df.toPandas()["SupplierId"][0] == expected