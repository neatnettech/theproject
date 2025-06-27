from staging.models import Acceptance
from sqlalchemy.orm import Session
from typing import List


class AcceptanceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_acceptance_events_by_manifest(self, changeset: str, record: str):
        return self.db.query(Acceptance)\
            .filter(Acceptance.changeset_id == changeset, Acceptance.record == record)\
            .order_by(Acceptance.record.asc())\
            .all()
            
    def get_all_changes(self) -> List[Acceptance]:
        return self.db.query(Acceptance).order_by(Acceptance.created_at.desc()).all()