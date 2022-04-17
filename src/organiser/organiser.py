"""Contains the class for organising all participants into teams"""

import utilities.definitions as definitions


class Organiser:
    """
    Randomly and fairly groups participants into teams based on given requirements.

    Constants
    ----------
    COL_ASSIGNED: str
        Defined name for assigned column. This is a flag to indicate if a participant has already been assigned to a
        team or not.

    Parameters
    -----------
    participants: DataFrame
        Data on participants to be grouped.

    Methods
    ----------
    organise():
        Main method to distribute participants into teams

    """

    COL_ASSIGNED = "assigned"

    def __init__(self, participants):
        self.participants = participants

    def _create_assigned_column(self):

        assigned = [False for i in range(len(self.participants))]

        self.participants[self.COL_ASSIGNED] = assigned

    def _remove_assigned_column(self):
        self.participants.drop(self.COL_ASSIGNED, inplace=True, axis=1)

    def organise(self, num_teams):
        """
        Distributes participants into teams

        Parameters
        ----------
        num_teams: int
            Number of teams to create. Participants will be distributed as fairly as possible.

        Returns
        ----------
        A list of teams, where each team contains a list of participant records.
        """

        self._create_assigned_column()
        remaining_participants = self.participants.copy(deep=True)
        teams = [[] for i in range(num_teams)]

        # Raise error if number of participants are fewer than number of required teams.
        if num_teams > len(self.participants):
            raise ValueError(definitions.too_many_teams_msg(num_teams, len(self.participants)))

        team_counter = 0
        while not remaining_participants.empty:
            sample_member = remaining_participants.sample()
            sample_index = sample_member.index[0]

            member = [sample_member.at[sample_index, "name"], sample_member.at[sample_index, "cluster"]]
            teams[team_counter].append(member)

            # Remove participants from pool
            remaining_participants.drop(inplace=True, index=sample_index, axis=0)
            self.participants.loc[(self.participants["name"] == member[0]), self.COL_ASSIGNED] = True

            # Update team_counter
            team_counter += 1
            if team_counter == num_teams:
                team_counter = 0

        self._remove_assigned_column()
        return teams
