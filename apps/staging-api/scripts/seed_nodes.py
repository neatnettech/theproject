from app.database import get_engine, get_session_factory, init_db
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

def main():
    engine = get_engine()
    init_db(engine)
    session_factory = get_session_factory(engine)
    session = session_factory()

    try:
        seed_market_record(session)
        session.commit()
        print("✅ Seed completed.")
    except Exception as e:
        session.rollback()
        print(f"❌ Seed failed: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    main()