import datetime
import typer
from typing import List, Optional, Tuple

from ser.model import Location, Factors
from ser.cbb.data import load_teams, load_bracket
from ser.cbb.game import CBBGame
from ser.cbb.rank import rank_teams
from ser.cbb.predict import predict_game, predict_bracket

app = typer.Typer()


@app.command()
def rank(year: Optional[int] = None, factor: Optional[List[str]] = typer.Option(None)):
    if not year:
        year = str(datetime.date.today().year)

    teams = load_teams(year)

    rankings = rank_teams(teams, Factors.from_list(factor))
    ranking = 1
    for team, rating in rankings:
        print(f"{ranking}. {team} - {rating}")
        ranking += 1


@app.command()
def predict(team: str, opponent: str, year: Optional[int] = None, location: Optional[str] = "H", factor: Optional[List[str]] = typer.Option(None)):
    if not year:
        year = str(datetime.date.today().year)

    teams = load_teams(year)

    if location.upper() == "H":
        location = Location.HOME
    elif location.upper() == "A":
        location = Location.AWAY
    elif location.upper() == "N":
        location = Location.NEUTRAL

    prediction = predict_game(teams, team, opponent, location, Factors.from_list(factor))
    print(prediction)


@app.command()
def bracket(year: Optional[int] = None, factor: Optional[List[str]] = typer.Option(None)):
    if not year:
        year = str(datetime.date.today().year)

    teams = load_teams(year)
    bracket = load_bracket(year)

    bracket_odds = predict_bracket(teams, bracket, Factors.from_list(factor))
    for team, bracket, seed, rating, odds in bracket_odds:
        print(seed, end="\t")
        print(team, end="\t")
        print(rating, end="\t")
        print(bracket, end="\t")
        for o in odds:
            print(o, end="\t")
        print()
