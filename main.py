from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from sqlmodel import Session, select
from sqlalchemy import func
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
            select(People.nameFirst, People.nameLast, People.playerID)
            .join(Batting, Batting.playerID == People.playerID)
            .where(Batting.yearID == year, Batting.teamID == team)
        ).all()
    # Return a list of dictionaries with explicit keys for the frontend
    players = [
        {"first_name": row[0], "last_name": row[1], "playerID": row[2]} for row in rows
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

@app.get("/Bio")
async def get_Bio(playerID: str):
    with Session(engine) as session:
        rows = session.exec(
            select(People.nameFirst, People.nameLast, People.birthYear, People.birthMonth, People.birthDay,People.birthState, People.birthCity, People.height, People.weight)
            .where(People.playerID == playerID)
        ).all()
    # Return a list of dictionaries with explicit keys for the frontend
    bio = [
        {"first_name": row[0], "last_name": row[1], "birth_year": row[2], "birth_month": row[3], "birth_day": row[4], "birth_state": row[5], "birth_city": row[6], "height": row[7], "weight": row[8]} for row in rows
    ]
    return bio

#Endpoint to get carrer stats for a player
@app.get("/Stats")
async def get_Stats(playerID: str):
    with Session(engine) as session:
        rows = session.exec(
            select(
                func.sum(Batting.G),
                func.sum(Batting.H),
                func.sum(Batting.RBI),
                func.sum(Batting.SB),
            ).group_by(Batting.playerID)
            .where(Batting.playerID == playerID)
        ).all()
    # Return a list of dictionaries with explicit keys for the frontend
    stats = [
        {"games_played": row[0], "hits": row[1], "rbi": row[2], "stolen_bases": row[3]} for row in rows
    ]
    return stats

app.mount("/", StaticFiles(directory="static", html=True), name="static")