from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from sqlmodel import Session, select
from models import engine, People, Team, Batting

app = FastAPI()


@app.get("/years")
async def get_years():
	with Session(engine) as session:
		years = session.exec(select(Team.yearID).distinct().order_by(Team.yearID)).all()
	return years


app.mount("/", StaticFiles(directory="static", html=True), name="static")