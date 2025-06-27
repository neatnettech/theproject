from dataclasses import dataclass

@dataclass
class GetAcceptanceQuery:
    record_key: str
    
@dataclass(frozen=True)
class GetAllAcceptanceChangesQuery:
    pass