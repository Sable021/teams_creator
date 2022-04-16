import pandas as pd
import pytest

from src.reader.csv_reader import CsvReader

TEST_PATH = "./tests/test_data/"
TEST_FILE_SINGLE = "test_participants_single.csv"
TEST_FILE = "test_participants.csv"
TEST_SINGLE = pd.read_csv(TEST_PATH + TEST_FILE_SINGLE)
TEST_PARTICIPANTS = pd.read_csv(TEST_PATH + TEST_FILE)


@pytest.fixture
def new_reader():
    """Returns new instance of LocalCsvReader"""

    return CsvReader(TEST_PATH)


def test_read_sample_test_file(new_reader):
    actual_singles = new_reader.read_file(TEST_FILE_SINGLE)
    assert actual_singles.equals(TEST_SINGLE)

    actual_partipants = new_reader.read_file(TEST_FILE)
    assert actual_partipants.equals(TEST_PARTICIPANTS)


def test_get_participants(new_reader):
    test_participants = new_reader.read_file(TEST_FILE)
    assert test_participants.equals(TEST_PARTICIPANTS)

    actual = new_reader.get_participants()
    assert actual.equals(TEST_PARTICIPANTS)
