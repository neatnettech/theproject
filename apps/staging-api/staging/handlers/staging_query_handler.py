from sqlalchemy.orm import Session
from staging.models import Staging
from staging.queries.staging_queries import GetStagingQuery, GetAllStagingChangesQuery
from typing import List


class StagingQueryHandler:
    def __init__(self, db: Session):
        self.db = db

    def handle_get_staging(self, query: GetStagingQuery) -> list[Staging]:
        return (
            self.db.query(Staging)
            .filter(Staging.record_key == query.record_key)
            .order_by(Staging.current_revision.desc())
            .all()
        )
        
    def handle(self, query: GetAllStagingChangesQuery) -> List[Staging]:
        return (
            self.db.query(Staging).all()
        )