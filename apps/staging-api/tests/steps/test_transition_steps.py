import json
from flask.testing import FlaskClient
from pytest_bdd import given, when, then, scenario
from app.models.core_model import Staging, ActionType, Status, ChangeSource
from app.utilz.changeset_id import generate_changeset_id
from conftest import test_logger

@scenario(
    "../features/transition_staging.feature",
    "Submit a staging change for review"
)
def test_submit_staging_change():
    pass


@given(
    'an existing staging change with record key "ID000000ABCD"',
    target_fixture="existing_change",
)
def create_staging_change(db_session) -> Staging:
    test_logger.debug(f"Session ID: {id(db_session)}")
    record_key = "ID000000ABCD"
    change = Staging(
        record_key=record_key,
        directory="SAPA",
        action=ActionType.CREATE,
        new_data={
            "record_key": record_key,
            "record_structure": "IDENTIFIER",
            "record_content_type": "D",
        },
        change_source=ChangeSource.USER,
        status=Status.INITIATED,
        current_revision=1,
        changeset_id=generate_changeset_id(),
        created_by="test_user"
    )
    db_session.add(change)
    db_session.commit()
    
    return change


@when('I POST to "/api/v1/staging/<change_id>/transition" with action "submit"')
def post_transition(client: FlaskClient, existing_change: Staging):
    body = {
        "action": "submit",
        "created_by": "test_user",
        "business_justification": "Test justification"
    }
    
    test_logger.debug(f"Posting to /api/v1/staging/{existing_change.record_key}/transition")
    
    client.response = client.post(
        f"/api/v1/staging/{existing_change.record_key}/transition",
        data=json.dumps(body),
        content_type="application/json",
    )
    test_logger.debug(client.response.get_data(as_text=True))


@then("the response status code should be 200")
def check_status_code(client: FlaskClient):
    test_logger.debug(f"Response status code: {client.response.status_code}")
    assert client.response.status_code == 200


@then('the response should contain "Transition \'submit\' applied successfully."')
def check_response_text(client: FlaskClient):
    test_logger.debug(f"Response body: {client.response.get_data(as_text=True)}")
    assert "Transition 'submit' applied successfully." in client.response.get_data(
        as_text=True
    )