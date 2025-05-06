from dataclasses import dataclass

@dataclass
class GetStagingQuery:
    record_key: str
    
@dataclass(frozen=True)
class GetAllStagingChangesQuery:
    pass