"""Local CSV Reader Class"""

import pandas as pd


class CsvReader:
    """
    Reads CSV files for to obtain participant information based on a local path folder.

    Parameters
    ----------
    data_path: str
        file folder path

    participants: DataFrame
        Stores all read in information of participants

    Methods
    ----------
    read_file(file=str):
        Reads the CSV file and returns the list of participants.

    get_participants():
        Gets a list of participants already read by the reader

    """

    def __init__(self, local_path):
        self.local_path = local_path
        self.participants = pd.DataFrame()

    def read_file(self, file):
        """
        Reads the CSV file stored by the class and returns the list of participants.
        Rewrites the local participants Dataframe.

        Returns
        ----------
            particpants (DataFrame): Participants information.

        """
        full_file_path = self.local_path + file
        self.participants = pd.read_csv(full_file_path)

        return self.participants

    def get_participants(self):
        """
        Returns the cached DataFrame of participants

        Returns
        ----------
            participants (DataFrame): Participants information
        """

        return self.participants
