Quick DB setup

1. Create SQLite DB and load CSVs:

   python3 load_data.py

2. The script will create `baseball.db` in the repository root, apply `schema.sql`,
   and import `people.csv`, `teams.csv`, and `Batting.csv`.

Notes:
- Primary keys applied:
  - `people`: `playerID`
  - `teams`: composite `(teamID, yearID)`
  - `batting`: composite `(playerID, yearID, stint)`
- Foreign keys:
  - `batting.playerID` -> `people.playerID`
  - `batting.(teamID, yearID)` -> `teams.(teamID, yearID)`

If you want me to run the loader here, tell me and I'll run it and report any errors.