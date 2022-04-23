import os
import pandas as pd
import pytest

from src.input_output.csv_writer import CsvTeamsWriter
from tests.test_organiser.test_organiser_cluster import NUM_TEST_PARTICIPANTS

# Tests Setup
NUM_CLUSTERS = 4
NUM_TEAMS = 3


def create_test_teams():
    test_teams = []
    member_counter = 0
    for i in range(NUM_TEAMS):
        team = []
        for j in range(NUM_CLUSTERS):
            member = [f"Member {member_counter}", f"Cluster {j}"]
            member_counter += 1
            team.append(member)
        test_teams.append(team)

    return test_teams


TEST_TEAMS = create_test_teams()
TEST_PATH = "./tests/test_data/"
TEST_FILE = "test_output.csv"

# Unit Tests
def assert_test_output_format(file_full_path):
    """Tests that the output file has content in the expected format"""
    output_teams = pd.read_csv(file_full_path)

    # Only 3 Columns: Team, Name, Cluster
    expected_columns = ["team", "name", "cluster"]
    output_columns = output_teams.columns.tolist()

    assert output_columns == expected_columns

    # Number of rows == NUM_TEST_PARTICIPANTS
    assert len(output_teams) == NUM_TEST_PARTICIPANTS


@pytest.fixture
def tested():
    return CsvTeamsWriter(TEST_PATH, TEST_TEAMS)


def test_write_test_teams(tested):
    tested.write_file(TEST_FILE)
    full_output_path = TEST_PATH + TEST_FILE

    assert os.path.exists(full_output_path)
    assert_test_output_format(full_output_path)

    # Delete output file
    os.remove(full_output_path)
