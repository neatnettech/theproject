import os
import tempfile
from staging.handlers.staging_query_handler import StagingQueryHandler
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Body
from dependency_injector.wiring import inject, Provide
from staging.commands.staging_commands import TransitionCommand, BuildProjectionCommand
from staging.containers import Container
from staging.handlers.staging_command_handler import AcceptanceCommandHandler, StagingCommandHandler
from staging.acquisition.importer import process_directory_file
from staging.queries.staging_queries import GetStagingQuery, GetAllStagingChangesQuery
from staging.handlers.projection_command_handler import ProjectionQueryHandler

staging_router = APIRouter(
    prefix="/staging", tags=["staging"]
)

@staging_router.get("/")
def index():
    return {"message": "Staging API v1"}


@staging_router.post("/import/{directory_name}/{change_source}")
@inject
def import_directory(
    directory_name: str,
    change_source: str,
    file: UploadFile = File(...),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No selected file")

    filename = os.path.basename(file.filename)
    temp_file_path = os.path.join(tempfile.gettempdir(), filename)

    with open(temp_file_path, "wb") as buffer:
        buffer.write(file.file.read())

    try:
        process_directory_file(temp_file_path, directory_name, change_source)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": f"Data imported for directory {directory_name}"}


@staging_router.post("/{record}/{changeset}/transition")
@inject
def transition_staging_change(
    record: str,
    changeset: str,
    body: dict = Body(...),
    handler: AcceptanceCommandHandler = Depends(
        Provide[Container.staging_command_handler]
    ),
):
    action = body.get("action")
    created_by = body.get("created_by")
    business_justification = body.get("business_justification")

    if not action or not created_by or not business_justification:
        raise HTTPException(status_code=400, detail="Missing required fields")

    try:
        command = TransitionCommand(
            record=record,
            changeset=changeset,
            action=action,
            created_by=created_by,
            business_justification=business_justification,
        )

        result = handler.transition_staging(command)

        return {
            "record": record,
            "changeset": changeset,
            "new_status": result.status.value,
            "created_by": created_by,
            "business_justification": business_justification,
            "message": f"Transition '{action}' applied successfully.",
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@staging_router.get("/changeset/{changeset_id}/record/{record_id}/projection")
@inject
def get_manifest_projection(
    changeset_id: str,
    record_id: str,
    handler: ProjectionQueryHandler = Depends(
        Provide[Container.projection_query_handler]
    ),
):
    try:
        command = BuildProjectionCommand(changeset_id=changeset_id, record_id=record_id)
        result = handler.handle(command)
        return {
            "changeset_id": changeset_id,
            "record_id": record_id,
            "projection": result,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@staging_router.get("/changes", tags=["staging"])
@inject
def get_all_staging_changes(
    handler: StagingQueryHandler = Depends(Provide[Container.staging_query_handler]),
):
    try:
        query = GetAllStagingChangesQuery()
        result = handler.handle(query)
        return {"changes": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@staging_router.get("/{record_key}")
@inject
def get_staging(
    record_key: str,
    handler: StagingQueryHandler = Depends(Provide[Container.staging_query_handler]),
):
    query = GetStagingQuery(record_key=record_key)
    changes = handler.handle_get_staging(query)

    if not changes:
        raise HTTPException(
            status_code=404, detail="No staging changes found for this record_key"
        )

    results = [
        {
            "record_key": change.record_key,
            "chageset_id": change.changeset_id,
            "directory": change.directory,
            "action": change.action.value,
            "new_data": change.new_data,
            "change_source": change.change_source.value,
            "status": change.status.value,
            "current_revision": change.current_revision,
            "created_at": change.created_at.isoformat(),
        }
        for change in changes
    ]

    return {"record_key": record_key, "staging_changes": results}
