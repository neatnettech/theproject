import os
from pytest_bdd import given, when, then, scenario
from flask.testing import FlaskClient
from conftest import test_logger

@scenario("../features/import_staging.feature", "Import a directory file")
def test_import_file():
    pass


@given('a valid CSV file "tests/test_data/sample.csv"', target_fixture="valid_csv_file")
def valid_csv_file():
    return os.path.abspath("tests/test_data/sample.csv")


@when('I POST it to "/api/v1/staging/import/SAPA/USER"')
def post_file(client: FlaskClient, valid_csv_file):
    with open(valid_csv_file, "rb") as f:
        data = {"file": (f, "sample.csv")}
        client.response = client.post(
            "/api/v1/staging/import/SAPA/USER", data=data, content_type="multipart/form-data"
        )
        test_logger.debug(f"Response: {client.response.get_data(as_text=True)}")


@then("the response status code should be 200")
def check_status_code(client: FlaskClient):
    test_logger.debug(f"Response status code: {client.response.status_code}")
    assert client.response.status_code == 200


@then('the response should contain "Data imported for directory SAPA"')
def check_response_body(client: FlaskClient):
    test_logger.debug(f"Response body: {client.response.get_data(as_text=True)}")
    assert "Data imported for directory SAPA" in client.response.get_data(as_text=True)
