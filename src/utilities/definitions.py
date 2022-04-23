"""This module contains all pre-defined constants used throughout the application."""

# Error Messages
def too_many_teams_msg(num_teams, num_participants):
    """Number of teams is greater than number of participants."""
    return f"{num_teams} teams is too many for {num_participants} participants."


def zero_cluster_per_team():
    """Nobody from any cluster can join any team. All teams will have 0 members."""
    return "Cluster_per_team is set to 0. All teams will have 0 members."


def cluster_per_team_too_low(cluster_per_team, num_teams):
    """Maximum number of members from the same cluster is too low to fully distribute participants."""
    return f"cluster_per_team value of {cluster_per_team} is too low to successfully form {num_teams} teams."
