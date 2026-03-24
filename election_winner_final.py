#!/usr/bin/env python3
"""
Date: March 23rd, 2026

Author: Elias Mahdi (1373400)

Question 1 - CIS*2250 Milestone III
How did the winning political party change between the 43rd and 44th federal
elections in a selected province?

this script extracts the winning party from each riding's elected
candidate field, counts how many ridings each party won in the selected province,
and then identifies the province-level winner as the party with the most riding
wins in that province.
"""

import csv
import sys
import unicodedata

FILE_2019 = "data/election43_table11.csv"
FILE_2021 = "data/election44_table11.csv"


def normalize_province(name):
    name = name.strip().lower()
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    return name


def get_party(candidate):
    if "Bloc Québécois" in candidate:
        return "Bloc Quebecois"
    elif "New Democratic Party" in candidate or "NDP-New Democratic Party" in candidate:
        return "New Democratic Party"
    elif "Green Party" in candidate:
        return "Green Party"
    elif "Liberal/" in candidate:
        return "Liberal Party"
    elif "Conservative/" in candidate:
        return "Conservative Party"
    elif "Independent/" in candidate:
        return "Independent"
    else:
        return "Unknown"


def count_party_wins(filename, selected_province):
    party_wins = {}

    with open(filename, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            province_in_file = row["Province"].split("/")[0].strip()

            if normalize_province(province_in_file) == normalize_province(selected_province):
                candidate = row["Elected Candidate/Candidat élu"]
                party = get_party(candidate)

                if party in party_wins:
                    party_wins[party] += 1
                else:
                    party_wins[party] = 1

    return party_wins


def get_winner(party_wins):
    winner = None
    max_seats = -1

    for party in party_wins:
        if party_wins[party] > max_seats:
            max_seats = party_wins[party]
            winner = party

    return winner


def print_table(wins_2019, wins_2021):
    parties = sorted(set(wins_2019.keys()) | set(wins_2021.keys()))

    print("+------------------------+------------+------------+")
    print("| Party                  | 2019 Seats | 2021 Seats |")
    print("+------------------------+------------+------------+")

    for party in parties:
        seats_2019 = wins_2019.get(party, 0)
        seats_2021 = wins_2021.get(party, 0)
        print(f"| {party:<22} | {seats_2019:>10} | {seats_2021:>10} |")

    print("+------------------------+------------+------------+")


def main():
    if len(sys.argv) != 2:
        print("Usage: python election_winner_final.py <province>")
        sys.exit(1)

    province = sys.argv[1]

    wins_2019 = count_party_wins(FILE_2019, province)
    wins_2021 = count_party_wins(FILE_2021, province)

    if len(wins_2019) == 0 and len(wins_2021) == 0:
        print("Province not found.")
        sys.exit(1)

    winner_2019 = get_winner(wins_2019)
    winner_2021 = get_winner(wins_2021)

    print("\nProvince:", province)
    print()
    print_table(wins_2019, wins_2021)

    print("\n2019 Winner:", winner_2019)
    print("2021 Winner:", winner_2021)

    if winner_2019 == winner_2021:
        print("\nResult: The winning party remained the same.")
    else:
        print("\nResult: The winning party changed.")


if __name__ == "__main__":
    main()
