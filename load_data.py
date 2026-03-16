#!/usr/bin/env python3
"""
Simple loader: creates SQLite DB `baseball.db`, applies `schema.sql`,
and imports `people.csv`, `teams.csv`, and `Batting.csv`.

Usage:
  python3 load_data.py

This script tries to infer column names from CSV headers and insert rows.
Empty fields are stored as NULL. Foreign keys are enabled.
"""
import sqlite3
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent
DB = BASE / "baseball.db"
SCHEMA = BASE / "schema.sql"
CSVS = {
    'people': BASE / 'people.csv',
    'teams': BASE / 'teams.csv',
    'batting': BASE / 'Batting.csv'
}


def apply_schema(conn):
    sql = SCHEMA.read_text()
    conn.executescript(sql)


def load_csv_into_table(conn, table, csv_path):
    if not csv_path.exists():
        print(f"Skipping {table}: {csv_path} not found")
        return
    with csv_path.open(newline='') as fh:
        reader = csv.reader(fh)
        headers = next(reader)
        cols = [h.strip() for h in headers]
        # Quote column names to allow names that start with digits or contain special chars
        quoted_cols = [f'"{c.replace("\"", "\"\"")}"' for c in cols]
        placeholders = ','.join('?' for _ in cols)
        q = f"INSERT OR REPLACE INTO {table} ({', '.join(quoted_cols)}) VALUES ({placeholders})"
        rows = []
        for r in reader:
            # Normalize empty strings to None so SQLite stores NULL
            rows.append([None if (c is None or c == '') else c for c in r])
        with conn:
            conn.executemany(q, rows)
        print(f"Loaded {len(rows)} rows into {table}")


def main():
    if DB.exists():
        print(f"Using existing DB: {DB}")
    conn = sqlite3.connect(str(DB))
    conn.execute('PRAGMA foreign_keys = ON;')
    apply_schema(conn)
    # load people and teams first to satisfy FK constraints
    load_csv_into_table(conn, 'people', CSVS['people'])
    load_csv_into_table(conn, 'teams', CSVS['teams'])
    load_csv_into_table(conn, 'batting', CSVS['batting'])
    conn.close()
    print('Done. Database created at', DB)


if __name__ == '__main__':
    main()
