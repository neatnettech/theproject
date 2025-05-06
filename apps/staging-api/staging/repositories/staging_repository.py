# /app/repositories/staging_repository.py
from staging.models import Staging
from sqlalchemy.orm import Session
from typing import List


class StagingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_staging_events_by_manifest(self, changeset_id: str, record_id: str):
        return self.db.query(Staging)\
            .filter(Staging.changeset_id == changeset_id, Staging.record_id == record_id)\
            .order_by(Staging.record_id.asc())\
            .all()
            
    def get_all_changes(self) -> List[Staging]:
        return self.db.query(Staging).order_by(Staging.created_at.desc()).all()