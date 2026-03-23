from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from sqlmodel import Session, select
from models import engine, Batting, People, Teams

app = FastAPI()

@app.get("/years")
async def get_years():
    with Session(engine) as session:
        years = session.exec(select(Teams.yearID).distinct().order_by(Teams.yearID)).all()
    return years

@app.get("/players")
async def get_players(year: int, team: str):
    with Session(engine) as session:
        rows = session.exec(
            select(People.nameFirst, People.nameLast)
            .join(Batting, Batting.playerID == People.playerID)
            .where(Batting.yearID == year, Batting.teamID == team)
        ).all()
    # Return a list of dictionaries with explicit keys for the frontend
    players = [
        {"first_name": row[0], "last_name": row[1]} for row in rows
    ]
    return players

@app.get("/teams")
async def get_teams(year: int):
    with Session(engine) as session:
        rows = session.exec(
            select(Teams.name, Teams.divID, Teams.lgID, Teams.teamID).where(Teams.yearID == year)
        ).all()
    # Return a list of dictionaries with explicit keys for the frontend
    teams = [
        {"name": row[0],"league": row[2], "division": row[1], "team_id": row[3]} for row in rows
    ]
    return teams


app.mount("/", StaticFiles(directory="static", html=True), name="static")