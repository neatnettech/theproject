# /app/services/projection_service.py
from staging.repositories.staging_repository import StagingRepository
from staging.models.core_model import ActionType, ThomsonRecord

class ProjectionService:
    def __init__(self, staging_repository: StagingRepository):
        self.repo = staging_repository

    def build_projection(self, changeset_id: str, record_id: str) -> dict:
        events = self.repo.get_staging_events_by_manifest(changeset_id, record_id)
        projection = {}

        last_gs = {}
        last_new = {}

        for event in sorted(events, key=lambda e: e.revision):
            new_data = event.market_record_json_new or {}
            gs_data = event.market_record_json_gs or {}

            if event.action == ActionType.CREATE:
                projection = new_data.copy()

            elif event.action == ActionType.UPDATE:
                projection.update(new_data)

            elif event.action == ActionType.DELETE:
                projection = {}

            # Capture latest gs/new for diff computation
            if event.revision == events[-1].revision:
                last_gs = gs_data
                last_new = new_data

        # Compute diff using ThomsonRecord
        diff = {}
        if last_gs and last_new:
            try:
                gs_rec = ThomsonRecord.from_raw(last_gs)
                new_rec = ThomsonRecord.from_raw(last_new)
                diff = new_rec.diff(gs_rec)
            except Exception as e:
                diff = {"error": f"diff failed: {str(e)}"}

        return {
            "projection": projection,
            "diff": diff
        }