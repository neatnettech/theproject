import csv
from datetime import datetime
from typing import List
from staging.models import MarketRecord, ThomsonRecord


def parse_market_directory_json(file_path: str) -> List[MarketRecord]:
    import json

    with open(file_path, "r") as f:
        data = json.load(f)

    records = []
    for item in data:
        thomson_record = ThomsonRecord.from_raw(item)
        record = MarketRecord(
            record_id=thomson_record.file_key,
            record_value=thomson_record.to_record_value()
        )
        records.append(record)

    return records
