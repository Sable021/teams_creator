"""Contains the class for organising all participants into teams"""
import pandas as pd
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
    organise(num_teams: int, cluster_per_team: int):
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

    def _update_team_counter(self, counter, num_teams):
        counter += 1
        if counter == num_teams:
            counter = 0

        return counter

    def organise(self, num_teams, cluster_per_team):
        """
        Distributes participants into teams

        Parameters:
        ----------
        num_teams: int
            Number of teams to create. Participants will be distributed as fairly as possible.

        cluster_per_team: int
            Maximum number of partcipants in a team belonging to the same cluster.

        Returns
        ----------
        list: A list of teams, where each team contains a list of team members in form [member_name, cluster_name].
        """

        self._create_assigned_column()
        remaining_participants = self.participants.copy(deep=True)
        teams = [[] for i in range(num_teams)]
        clusters = self.participants["cluster"].unique()
        num_clusters = len(clusters)

        np_meta = [[0] * num_clusters] * num_teams
        teams_meta = pd.DataFrame(np_meta, columns=self.participants["cluster"].unique())

        # Raise error if number of participants are fewer than number of required teams.
        if num_teams > len(self.participants):
            raise ValueError(definitions.too_many_teams_msg(num_teams, len(self.participants)))

        # Raise error if cluster_per_team is set to 0
        if cluster_per_team == 0:
            raise ValueError(definitions.zero_cluster_per_team())

        # Raise error if cluster_per_team and num_teams will result in impossible team distribution
        num_members_per_team = int(len(self.participants) / num_teams)
        if cluster_per_team * num_clusters < num_members_per_team:
            raise ValueError(definitions.cluster_per_team_too_low(cluster_per_team, num_teams))

        team_counter = 0
        while not remaining_participants.empty:
            sample_member = remaining_participants.sample()
            sample_index = sample_member.index[0]

            # Check if current team can accept cluster member
            member_cluster = sample_member.at[sample_index, "cluster"]
            while teams_meta.loc[team_counter, member_cluster] >= cluster_per_team:
                # Update team_counter
                team_counter = self._update_team_counter(team_counter, num_teams)

            member = [sample_member.at[sample_index, "name"], member_cluster]
            teams[team_counter].append(member)

            # Update teams_meta
            teams_meta.loc[team_counter, member_cluster] += 1

            # Remove participants from pool
            remaining_participants.drop(inplace=True, index=sample_index, axis=0)
            self.participants.loc[(self.participants["name"] == member[0]), self.COL_ASSIGNED] = True

            # Update team_counter
            team_counter = self._update_team_counter(team_counter, num_teams)

        self._remove_assigned_column()
        return teams
