from staging.models import Status
from transitions import Machine

states = [
    "initiated",
    "pending review",
    "under review",
    "accepted",
    "rejected",
]

transitions = [
    {"trigger": "submit", "source": "initiated", "dest": "pending review"},
    {"trigger": "start_review", "source": "pending review", "dest": "under review"},
    {"trigger": "approve", "source": ["pending review", "under review"], "dest": "accepted"},
    {"trigger": "reject", "source": ["pending review", "under review"], "dest": "rejected"},
]

class AcceptanceWorkflow:
    def __init__(self, initial_state: str):
        self.state = initial_state
        self.machine = Machine(
            model=self,
            states=states,
            transitions=transitions,
            initial=self.state,
            auto_transitions=False,
        )

class AcceptanceWorkflowService:
    # def transition(self, staging: Staging, action: str) -> Status:
    #     workflow = StagingWorkflow(staging.status.value)
    #     if not hasattr(workflow, action):
    #         raise ValueError(f"Invalid transition action: {action}")
    #     getattr(workflow, action)()
    #     staging.status = Status(workflow.state)
    #     return staging.status
    
    
    def transition(self, current_status: Status, action: str) -> Status:
        workflow = AcceptanceWorkflow(current_status.value)
        if not hasattr(workflow, action):
            raise ValueError(f"Invalid transition action: {action}")
        getattr(workflow, action)()
        return Status(workflow.state)