import pandas as pd
import pytest

from src.organiser.organiser import Organiser

# Test setups
def create_test_participants():
    participant_1 = ["Wong Fu Jie", "AI Engineering"]
    participant_2 = ["Ang Wee Kiat Robin", "Centre of Excellence"]
    participant_3 = ["Desmond Tan Zhi Heng", "Navy C3"]
    participant_4 = ["Ong Kai Yong", "Autonomy"]
    participant_5 = ["Koh Hui Wen", "Computer Vision"]
    participant_6 = ["Derek Chew", "NLP"]

    participants = [participant_1, participant_2, participant_3, participant_4, participant_5, participant_6]

    participants_df = pd.DataFrame(participants, columns=["name", "cluster"])

    return participants_df


TEST_PARTICIPANTS = create_test_participants()


@pytest.fixture
def tested():
    return Organiser(TEST_PARTICIPANTS)


# Unit Tests
def assert_team_hold_unique_members(teams):
    """Tests that every member of a team is unique across teams.
    I.e., no participant belongs to more than 1 team."""
    for i in range(len(teams)):
        team_to_test = teams[i]
        for team_member in team_to_test:
            for j in range(len(teams)):
                if j != i:
                    assert (team_member in teams[j]) == False


def test_distribute_to_one_group(tested):
    """Create 1 team to hold all participants"""
    teams = tested.organise(num_teams=1)

    assert len(teams) == 1
    assert_team_hold_unique_members(teams)


def test_distribute_one_per_group(tested):
    """Number of teams equal to number of participants. 1 unique participant per team."""

    expected_num_teams = len(TEST_PARTICIPANTS)
    teams = tested.organise(num_teams=expected_num_teams)

    assert len(teams) == expected_num_teams

    # Each team should only have one member
    for team in teams:
        assert len(team) == 1

    assert_team_hold_unique_members(teams)


def test_distribute_less_teams_than_participants(tested):
    """Distribute test participants to 2 teams. Each team should have 2 members."""

    expected_num_teams = 2
    teams = tested.organise(num_teams=expected_num_teams)

    # Expect only 2 teams
    assert len(teams) == 2

    # Each team should have 3 members
    for team in teams:
        assert len(team) == 3

    assert_team_hold_unique_members(teams)


def test_distribute_less_teams_than_participants_uneven(tested):
    """Distribute test participants to non-divisible number of teams."""
    expected_num_teams = 4
    teams = tested.organise(num_teams=expected_num_teams)

    # Expect only 4 teams
    assert len(teams) == 4

    # Each team has at most 2 members
    for team in teams:
        assert len(team) <= 2

    assert_team_hold_unique_members(teams)


def test_expection_when_teams_more_than_participants(tested):
    num_teams = len(TEST_PARTICIPANTS) + 1

    with pytest.raises(ValueError):
        teams = tested.organise(num_teams=num_teams)
