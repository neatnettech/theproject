from staging.state.staging_state_machine import StagingWorkflow
from staging.models.core_model import Staging, Status


class StagingWorkflowService:
    # def transition(self, staging: Staging, action: str) -> Status:
    #     workflow = StagingWorkflow(staging.status.value)
    #     if not hasattr(workflow, action):
    #         raise ValueError(f"Invalid transition action: {action}")
    #     getattr(workflow, action)()
    #     staging.status = Status(workflow.state)
    #     return staging.status
    
    
    def transition(self, current_status: Status, action: str) -> Status:
        workflow = StagingWorkflow(current_status.value)
        if not hasattr(workflow, action):
            raise ValueError(f"Invalid transition action: {action}")
        getattr(workflow, action)()
        return Status(workflow.state)