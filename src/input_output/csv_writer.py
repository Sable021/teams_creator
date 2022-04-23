"""Contains class to write the created teams into file."""
import pandas as pd


class CsvTeamsWriter:
    """
    Writes all created teams into a .csv file.

    Parameters
    ----------
    path: str
        Folder path to store the output file.

    teams: list
        List of created teams with members. Assumptions include:
            1. List is correctly distributed.
            2. Contains a list of teams where each team is a list of members in the format [name, cluster]

    Methods
    ----------
    write_file(file: str):
        Writes the teams and members into a .csv file
    """

    def __init__(self, path, teams):
        self.path = path
        self.teams = teams

    def write_file(self, file):
        """
        Writes team distribution information into a file and saves it with the given file name.

        Parameters
        ----------
        file: str
            Output file name.
        """
        output_columns = ["team", "name", "cluster"]
        output_teams = pd.DataFrame(columns=output_columns)

        for i, team in enumerate(self.teams):
            for member in team:
                member.insert(0, i)
            output_team = pd.DataFrame(team, columns=output_columns)
            output_teams = pd.concat([output_teams, output_team], axis=0)

        output_full_path = self.path + file
        output_teams.to_csv(output_full_path, index=False)
