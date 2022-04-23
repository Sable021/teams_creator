from multiprocessing.sharedctypes import Value
from random import SystemRandom

import pandas as pd
import pytest

import src.utilities.definitions as definitions
from src.organiser.organiser import Organiser

# Test setups

NUM_TEST_PARTICIPANTS = 12


def create_test_participants(num_participants):
    participants = []

    # Will always set 3 members per cluster
    for i in range(num_participants):
        participant = [f"Member {i}", f"Cluster {int(i/3)}"]
        participants.append(participant)

    participants_df = pd.DataFrame(participants, columns=["name", "cluster"])

    return participants_df


TEST_PARTICIPANTS = create_test_participants(NUM_TEST_PARTICIPANTS)


@pytest.fixture
def tested():
    return Organiser(TEST_PARTICIPANTS)


# Unit Test
def assert_team_hold_unique_members(teams):
    """Tests that every member of a team is unique across teams.
    I.e., no participant belongs to more than 1 team."""
    for i in range(len(teams)):
        team_to_test = teams[i]
        for team_member in team_to_test:
            for j in range(len(teams)):
                if j != i:
                    assert (team_member in teams[j]) == False


def assert_cluster_members_within_limit(teams, cluster_per_team):
    """Test each team has less than max number of members in the same cluster"""
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


def test_no_limit_cluster_per_team(tested):
    """Distribution will always succeed if cluster limit is equal or greater than num_participants"""

    # Generate cluster value always equal or greater than number of participants
    rand = SystemRandom()
    cluster_per_team = rand.randrange(start=len(TEST_PARTICIPANTS), stop=10000)
    num_teams = rand.randrange(start=1, stop=3)
    teams = tested.organise(num_teams, cluster_per_team)

    assert len(teams) == num_teams
    assert_team_hold_unique_members(teams)


def test_error_when_cluster_per_team_is_0(tested):
    """Error will be raised if cluster_per_team is set to 0. Nobody will be in any team"""

    rand = SystemRandom()
    num_teams = rand.randrange(start=1, stop=len(TEST_PARTICIPANTS))

    with pytest.raises(ValueError) as e:
        tested.organise(num_teams, 0)

    assert str(e.value) == definitions.zero_cluster_per_team()


def test_workable_cluster_value(tested):
    """Tests for workable and non-trivial cluster_per_team values."""

    cluster_per_team = 2
    # Team setup is always possible if number of teams >= 2
    rand = SystemRandom()
    num_teams = rand.randrange(start=2, stop=len(TEST_PARTICIPANTS))

    teams = tested.organise(num_teams, cluster_per_team)

    assert len(teams) == num_teams

    assert_team_hold_unique_members(teams)
    assert_cluster_members_within_limit(teams, cluster_per_team)


def test_workable_single_member_cluster(tested):
    """Tests for workable setup when cluster_per_team == 1"""

    cluster_per_team = 1
    # Team distribution is always possible if number of teams >= 4
    rand = SystemRandom()
    num_teams = rand.randrange(start=4, stop=len(TEST_PARTICIPANTS))

    teams = tested.organise(num_teams, cluster_per_team)

    assert len(teams) == num_teams

    assert_team_hold_unique_members(teams)
    assert_cluster_members_within_limit(teams, cluster_per_team)


def test_error_when_cluster_per_team_is_not_possible(tested):
    "Error will be raised if the cluster_per_team value makes team setup impossible"

    # Below parameters will make full distribution impossible.
    # Based on test participants.
    cluster_per_team = 1
    num_teams = 2

    with pytest.raises(ValueError) as e:
        teams = tested.organise(num_teams, cluster_per_team)

    assert str(e.value) == definitions.cluster_per_team_too_low(cluster_per_team, num_teams)


# Non-ideal unit test. Test outcomes must be specific and always reproducible!
def test_fair_dstribution_of_teams(tested):
    """
    Tests organiser will always create distirbutions that are as even as possible.

    N.B.: This test does not always produce the intended behaviour due to random nature of team distribution.
    """
    num_test_participants = 20
    num_clusters = 7
    participants = []
    for i in range(num_test_participants):
        cluster = int(i / (num_test_participants / num_clusters))
        participant = [f"Member {i}", f"Cluster {cluster}"]
        participants.append(participant)

    participants_df = pd.DataFrame(participants, columns=["name", "cluster"])
    print(participants_df)

    cluster_per_team = 1
    num_teams = 5
    tested = Organiser(participants_df)
    teams = tested.organise(num_teams, cluster_per_team)

    print(teams)

    expected_max_members = int(num_test_participants / num_teams) + 1
    for team in teams:
        assert 0 <= expected_max_members - len(team) <= 1
