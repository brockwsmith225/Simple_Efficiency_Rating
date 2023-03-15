import csv
from csv import DictReader
from typing import Dict

from ser.cbb.game import CBBGame
from ser.cbb.team import CBBTeam
from ser.model import Bracket


def load_teams(year: int) -> Dict[str, CBBTeam]:
    path = f"./Sports_Data_Scraper/cbb-{year}.csv"
    teams = dict()
    with open(path, "r") as f:
        csv_dict_reader = DictReader(f)
        for row in csv_dict_reader:
            if row["team"] not in teams:
                teams[row["team"]] = CBBTeam(
                    name=row["team"],
                    games=list(),
                )
            game = CBBGame(**row)
            teams[row["team"]].games.append(game)
    return teams


def load_bracket(year: int) -> Bracket:
    path = f"./Sports_Data_Scraper/cbb-{year}.bracket"
    brackets = []
    current_bracket_name = None
    with open(path, "r") as f:
        for line in f.readlines():
            if line.startswith("--"):
                current_bracket_name = line[2:]
                continue
            line = line.split("!")
            if line[0] == "*":
                bracket = Bracket(
                    subbracket_1=line[2].split("/")[0].strip(),
                    subbracket_2=line[2].split("/")[1].strip(),
                    seed_1=int(line[1]),
                    seed_2=int(line[1]),
                    bracket_name=current_bracket_name,
                )
            else:
                bracket = Bracket(
                    subbracket_1=line[2].strip(),
                    subbracket_2=None,
                    seed_1=int(line[1]),
                    seed_2=None,
                    bracket_name=current_bracket_name,
                )
            added = False
            for i in range(len(brackets)):
                if bracket.depth == brackets[i].depth:
                    brackets[i] = Bracket(
                        subbracket_1=brackets[i],
                        subbracket_2=bracket,
                        bracket_name=current_bracket_name,
                    )
                    while i > 0:
                        if brackets[i].depth == brackets[i-1].depth:
                            brackets[i-1] = Bracket(
                                subbracket_1=brackets[i-1],
                                subbracket_2=brackets[i],
                                bracket_name=current_bracket_name,
                            )
                            del brackets[i]
                            i -= 1
                        else:
                            break
                    added = True
                    break
            if not added:
                brackets.append(bracket)
    return brackets[0]
