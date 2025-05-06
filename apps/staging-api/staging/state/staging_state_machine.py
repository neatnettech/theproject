from transitions import Machine
from staging.state.staging_states import states, transitions

class StagingWorkflow:
    def __init__(self, initial_state: str):
        self.state = initial_state
        self.machine = Machine(
            model=self,
            states=states,
            transitions=transitions,
            initial=self.state,
            auto_transitions=False,
        )