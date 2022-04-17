import pandas as pd
import pytest

from src.organiser.organiser import Organiser

# Test setups

NUM_TEST_PARTICIPANTS = 10


def create_test_participants():
    participants = []

    for i in range(NUM_TEST_PARTICIPANTS):
        participant = [f"Member {i}", f"Cluster {i/2}"]
        participants.append(participant)

    participants_df = pd.DataFrame(participants, columns=["name", "cluster"])

    return participants_df


TEST_PARTICIPANTS = create_test_participants()


@pytest.fixture
def tested():
    return Organiser(TEST_PARTICIPANTS)


# Unit Test
