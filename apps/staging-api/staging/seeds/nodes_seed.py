from sqlalchemy.orm import Session
from staging.models import (
    MarketRecord,
    ThomsonRecord,
)
from uuid import uuid4


def seed_market_record(session):
    raw = {"file_key": "123091211111", "fwrnycr": "87q12632"}

    record = ThomsonRecord.from_raw(raw)

    market_record = MarketRecord(
        id=uuid4(),
        schema=None,
        url_to_blob=None,
        key_in_directory="init_seed",
        directory="test_directory",
        market_data_source="manual_seed",
        record_id=record.file_key,
        record_value=record.to_record_value(),
    )

    session.add(market_record)
    print(f"Seeded MarketRecord with record_id = {market_record.record_id}")