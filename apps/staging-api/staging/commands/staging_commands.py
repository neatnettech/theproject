from dataclasses import dataclass

@dataclass
class TransitionCommand:
    record_id: int
    action: str
    created_by: str = "system"
    business_justification: str = "No justification provided"
    
@dataclass
class BuildProjectionCommand:
    changeset_id: str
    record_id: str