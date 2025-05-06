from datetime import UTC, datetime
from sqlalchemy.orm import Session
from staging.commands.staging_commands import TransitionCommand
from staging.models.core_model import Staging, Status
from staging.services.staging_workflow_service import StagingWorkflowService


class StagingCommandHandler:
    def __init__(self, db: Session, workflow_service: StagingWorkflowService):
        self.db = db
        self.workflow_service = workflow_service

    def transition_staging(self, command: TransitionCommand) -> Staging:
        change = (
            self.db.query(Staging).filter_by(record_key=command.change_id).first()
        )

        if not change:
            raise ValueError(f"Staging change with ID {command.change_id} not found.")

        new_status = self.workflow_service.transition(change.status, command.action)
        new_rev = self._create_revision(change, new_status)

        self.db.add(new_rev)
        self.db.commit()
        return new_rev

    def _create_revision(self, prev: Staging, status: Status) -> Staging:
        return Staging(
            changeset_id=prev.changeset_id,
            record_key=prev.record_key,
            directory=prev.directory,
            action=prev.action,
            new_data=prev.new_data,
            change_source=prev.change_source,
            status=status,
            current_revision=prev.current_revision + 1,
            created_at=datetime.now(UTC),
        )
