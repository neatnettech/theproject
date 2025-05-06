from app.database import get_engine, get_session_factory, init_db
from app.seeds.nodes_seed import seed_market_record


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