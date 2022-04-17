from random import SystemRandom

import pandas as pd
import pytest

import src.utilities.definitions as definitions
from src.organiser.organiser import Organiser

# Test setups

NUM_TEST_PARTICIPANTS = 12


def create_test_participants():
    participants = []

    for i in range(NUM_TEST_PARTICIPANTS):
        participant = [f"Member {i}", f"Cluster {int(i/3)}"]
        participants.append(participant)

    participants_df = pd.DataFrame(participants, columns=["name", "cluster"])

    return participants_df


TEST_PARTICIPANTS = create_test_participants()


@pytest.fixture
def tested():
    return Organiser(TEST_PARTICIPANTS)


# Unit Test
def test_no_limit_cluster_per_team(tested):
    """Distribution will always succeed if cluster limit is equal or greater than num_participants"""

    # Generate cluster value always equal or greater than number of participants
    rand = SystemRandom()
    cluster_per_team = rand.randrange(start=len(TEST_PARTICIPANTS), stop=10000)
    num_teams = rand.randrange(start=1, stop=3)
    teams = tested.organise(num_teams, cluster_per_team)

    assert len(teams) == num_teams


def test_error_when_cluster_per_team_is_0(tested):
    """Error will be raised if cluster_per_team is set to 0. Nobody will be in any team"""

    rand = SystemRandom()
    num_teams = rand.randrange(start=1, stop=len(TEST_PARTICIPANTS))

    with pytest.raises(ValueError) as e:
        tested.organise(num_teams, 0)

    assert str(e.value) == definitions.zero_cluster_per_team()


def test_workable_cluster_value(tested):
    """Tests for workable and significant cluster_per_team values."""

    cluster_per_team = 2
    num_teams = 3
    # rand = SystemRandom()
    # num_teams = rand.randrange(start=2, stop=len(TEST_PARTICIPANTS))

    teams = tested.organise(num_teams, cluster_per_team)

    assert len(teams) == num_teams

    # Test each team has less than max number of members in the same cluster
    for team in teams:
        clusters = {}
        for member in team:
            cluster_name = member[1]
            if cluster_name in clusters:
                clusters[cluster_name] += 1
            else:
                clusters[cluster_name] = 1

        for key in clusters.keys():
            assert clusters[key] <= cluster_per_team
