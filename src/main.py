"""
Main teams creator module. Refer to readme.md for more information.

Assumptions
----------
1. File is always in "./src/data" folder

"""
import sys
from reader.csv_reader import CsvReader

DATA_FOLDER = "./src/data/"

# Assume data file is listed after python script
DATA_FILE = sys.argv[1]


def read_file():
    """Reads the file as read in the script arguments"""

    reader = CsvReader(DATA_FOLDER)
    participants = reader.read_file(DATA_FILE)
    print(participants)


def main():
    """MAIN FUNCTION"""
    read_file()


if __name__ == "__main__":
    main()
