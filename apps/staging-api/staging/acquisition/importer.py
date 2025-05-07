import uuid
from sqlalchemy.orm import Session
from staging.models import ActionType, Status, Staging, ThomsonRecord
from typing import Tuple, List, Dict
from staging.models import MarketRecord
from dependency_injector.wiring import inject, Provide
from staging.containers import Container
from staging.utilz.csv_reader import parse_market_directory_json
from staging.utilz.changeset_id import generate_changeset_id


@inject
def process_directory_file(
    file_path: str,
    directory: str,
    change_source: str,
    db_session: Session = Provide[Container.db_session],
):
    fi_data = parse_market_directory_json(file_path)

    new_records, updated_records, deleted_records = get_delta(fi_data)

    changeset_id = generate_changeset_id()

    for rec in new_records:
        current = (
            db_session.query(Staging)
            .filter(
                Staging.record_id == rec.record_id,
                Staging.directory == directory,
            )
            .order_by(Staging.revision.desc())
            .first()
        )
        new_revision = current.revision + 1 if current else 1

        # Wrap as ThomsonRecord for JSON projection
        record_json = ThomsonRecord.from_raw(rec.record_value).dict()

        staging = Staging(
            changeset_id=changeset_id,
            record_id=rec.record_id,
            directory=directory,
            action=ActionType.CREATE,
            market_record_json_new=record_json,
            change_source=change_source,
            status=Status.INITIATED,
            revision=new_revision,
        )
        db_session.add(staging)

    # --- UPDATEs ---
    for file_rec, db_rec in updated_records:
        current = (
            db_session.query(Staging)
            .filter(
                Staging.record_id == file_rec.record_id,
                Staging.directory == directory,
                Staging.action == ActionType.UPDATE,
            )
            .order_by(Staging.revision.desc())
            .first()
        )
        new_revision = current.revision + 1 if current else 1

        staging = Staging(
            changeset_id=changeset_id,
            record_id=file_rec.record_id,
            directory=directory,
            action=ActionType.UPDATE,
            market_record_json_new=ThomsonRecord.from_raw(file_rec.record_value).dict(),
            market_record_json_gs=ThomsonRecord.from_raw(db_rec.record_value).dict(),
            change_source=change_source,
            status=Status.INITIATED,
            revision=new_revision,
        )
        db_session.add(staging)

    db_session.commit()


def get_delta(
    file_records: List[MarketRecord],
    db_session: Session = Provide[Container.db_session],
) -> Tuple[
    List[MarketRecord], List[Tuple[MarketRecord, MarketRecord]], List[MarketRecord]
]:
    """
    Compares the given file MarketRecords against those in the DB.

    Returns:
        - new_records: not present in DB
        - updated_records: same record_id exists, value differs (tuple of file, db)
        - unchanged_records: identical in DB (excluded)
    """
    record_ids = [rec.record_id for rec in file_records]

    db_records = (
        db_session.query(MarketRecord)
        .filter(MarketRecord.record_id.in_(record_ids))
        .all()
    )

    db_by_id: Dict[str, MarketRecord] = {rec.record_id: rec for rec in db_records}

    new_records = []
    updated_records = []

    for rec in file_records:
        db_rec = db_by_id.get(rec.record_id)
        if db_rec is None:
            new_records.append(rec)
        elif db_rec.record_value != rec.record_value:
            updated_records.append((rec, db_rec))

    return new_records, updated_records, db_records
