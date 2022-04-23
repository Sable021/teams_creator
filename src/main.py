"""
Main teams creator module. Refer to readme.md for more information.

Assumptions
----------
1. File is always in "./src/data" folder

"""
import sys
from input_output.csv_reader import CsvReader
from input_output.csv_writer import CsvTeamsWriter
from organiser.organiser import Organiser

DATA_FOLDER = "./src/data/"

# Assume data file is listed after python script
DATA_FILE = sys.argv[1]
NUM_TEAMS = int(sys.argv[2])
CLUSTER_PER_TEAM = int(sys.argv[3])
OUTPUT_FILE = sys.argv[4]


def read_file(data_folder, data_file):
    """Reads the csv file as read in the script arguments"""

    reader = CsvReader(data_folder)
    participants = reader.read_file(data_file)
    return participants


def organise_teams(participants, num_teams, cluster_per_team):
    """Organsie"""
    organiser = Organiser(participants)
    teams = organiser.organise(num_teams, cluster_per_team)
    return teams


def write_file(folder_path, output_file, teams):
    """Outputs the resulting team distribution into a csv file based on provided file path and name."""
    writer = CsvTeamsWriter(folder_path, teams)
    writer.write_file(output_file)


def main():
    """MAIN FUNCTION"""
    participants = read_file(DATA_FOLDER, DATA_FILE)
    teams = organise_teams(participants, NUM_TEAMS, CLUSTER_PER_TEAM)

    print(f"Teams created. Outputting into {OUTPUT_FILE}.")
    write_file(DATA_FOLDER, OUTPUT_FILE, teams)


if __name__ == "__main__":
    main()
