"""Recreate the small synthetic ECS handoff from reviewable test records."""

import argparse
import json
from pathlib import Path
import sqlite3

from unified_knowledge.store import SCHEMA, canonical


def build_fixture(output):
    output = Path(output).resolve()
    if output.exists():
        raise ValueError("Choose a new fixture database path")
    records = Path(__file__).resolve().parents[1] / "assets/ecs-fixture/records.json"
    tables = json.loads(records.read_bytes())
    output.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(output)
    try:
        db.executescript(SCHEMA)
        for table, rows in tables.items():
            if table not in {
                "runs",
                "snapshots",
                "symbols",
                "relations",
                "anchors",
                "assets",
                "profiles",
                "meta",
            }:
                raise ValueError("Unexpected fixture table")
            for row in rows:
                columns = [r[1] for r in db.execute("PRAGMA table_info(" + table + ")")]
                values = [
                    canonical(row[k]) if k in {"data", "value"} else row[k]
                    for k in columns
                ]
                db.execute(
                    "INSERT INTO "
                    + table
                    + " VALUES("
                    + ",".join("?" for k in columns)
                    + ")",
                    values,
                )
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    build_fixture(parser.parse_args().output)
