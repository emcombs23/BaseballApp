from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel, create_engine
from sqlalchemy import Column, Integer, Float, String

database_url = "sqlite:///baseball.db"
engine = create_engine(database_url) 

class People(SQLModel, table=True):
	"""People model with all columns from `people.csv`."""
	ID: Optional[int] = Field(default=None)
	playerID: str = Field(primary_key=True, index=True)
	birthYear: Optional[int] = None
	birthMonth: Optional[int] = None
	birthDay: Optional[int] = None
	birthCity: Optional[str] = None
	birthCountry: Optional[str] = None
	birthState: Optional[str] = None
	deathYear: Optional[int] = None
	deathMonth: Optional[int] = None
	deathDay: Optional[int] = None
	deathCountry: Optional[str] = None
	deathState: Optional[str] = None
	deathCity: Optional[str] = None
	nameFirst: Optional[str] = None
	nameLast: Optional[str] = None
	nameGiven: Optional[str] = None
	weight: Optional[int] = None
	height: Optional[int] = None
	bats: Optional[str] = None
	throws: Optional[str] = None
	debut: Optional[str] = None
	bbrefID: Optional[str] = None
	finalGame: Optional[str] = None
	retroID: Optional[str] = None

	batting: List["Batting"] = Relationship(back_populates="player")


class Team(SQLModel, table=True):
	"""Teams model with all columns from `teams.csv` and composite PK (teamID, yearID)."""
	yearID: Optional[int] = Field(primary_key=True)
	lgID: Optional[str] = None
	teamID: Optional[str] = Field(default=None, primary_key=True)
	franchID: Optional[str] = None
	divID: Optional[str] = None
	Rank: Optional[int] = None
	G: Optional[int] = None
	Ghome: Optional[int] = None
	W: Optional[int] = None
	L: Optional[int] = None
	DivWin: Optional[str] = None
	WCWin: Optional[str] = None
	LgWin: Optional[str] = None
	WSWin: Optional[str] = None
	R: Optional[int] = None
	AB: Optional[int] = None
	H: Optional[int] = None
	Double: Optional[int] = Field(default=None, sa_column=Column("2B", Integer))
	Triple: Optional[int] = Field(default=None, sa_column=Column("3B", Integer))
	HR: Optional[int] = None
	BB: Optional[int] = None
	SO: Optional[int] = None
	SB: Optional[int] = None
	CS: Optional[int] = None
	HBP: Optional[int] = None
	SF: Optional[int] = None
	RA: Optional[int] = None
	ER: Optional[int] = None
	ERA: Optional[float] = None
	CG: Optional[int] = None
	SHO: Optional[int] = None
	SV: Optional[int] = None
	IPouts: Optional[int] = None
	HA: Optional[int] = None
	HRA: Optional[int] = None
	BBA: Optional[int] = None
	SOA: Optional[int] = None
	E: Optional[int] = None
	DP: Optional[int] = None
	FP: Optional[float] = None
	name: Optional[str] = None
	park: Optional[str] = None
	attendance: Optional[int] = None
	BPF: Optional[int] = None
	PPF: Optional[int] = None
	teamIDBR: Optional[str] = None
	teamIDlahman45: Optional[str] = None
	teamIDretro: Optional[str] = None

	batting: List["Batting"] = Relationship(back_populates="team")


class Batting(SQLModel, table=True):
	"""Batting model with all columns from `Batting.csv` and composite PK + FKs."""
	playerID: str = Field(foreign_key="people.playerID", primary_key=True)
	yearID: int = Field(foreign_key="teams.yearID", primary_key=True)
	stint: int = Field(primary_key=True)

	teamID: Optional[str] = Field(default=None, foreign_key="teams.teamID")
	lgID: Optional[str] = None
	G: Optional[int] = None
	AB: Optional[int] = None
	R: Optional[int] = None
	H: Optional[int] = None
	Double: Optional[int] = Field(default=None, sa_column=Column("2B", Integer))
	Triple: Optional[int] = Field(default=None, sa_column=Column("3B", Integer))
	HR: Optional[int] = None
	RBI: Optional[int] = None
	SB: Optional[int] = None
	CS: Optional[int] = None
	BB: Optional[int] = None
	SO: Optional[int] = None
	IBB: Optional[int] = None
	HBP: Optional[int] = None
	SH: Optional[int] = None
	SF: Optional[int] = None
	GIDP: Optional[int] = None

	player: Optional[People] = Relationship(back_populates="batting")
	team: Optional[Team] = Relationship(back_populates="batting")
