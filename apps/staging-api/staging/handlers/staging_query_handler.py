from sqlalchemy.orm import Session
from staging.models import Acceptance, Staging
from staging.queries.staging_queries import GetAcceptanceQuery, GetAllAcceptanceChangesQuery
from typing import List


class AcceptanceQueryHandler:
    def __init__(self, db: Session):
        self.db = db

    def handle_get_acceptance(self, query: GetAcceptanceQuery) -> list[Acceptance]:
        return (
            self.db.query(Staging)
            .filter(Staging.record_key == query.record_key)
            .order_by(Staging.current_revision.desc())
            .all()
        )
        
    def handle(self, query: GetAllAcceptanceChangesQuery) -> List[Staging]:
        return (
            self.db.query(Staging).all()
        )