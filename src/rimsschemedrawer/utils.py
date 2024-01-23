# Utility functions for the rims scheme drawer

import json
from pathlib import Path
from typing import Dict


def json_reader(fin: Path) -> Dict:
    """Read a json file and return a dictionary.

    This can take old or new files and return the data that
    can be read by the program.

    :return: Dictionary with parameters for drawing the scheme.
    """
    with open(fin, "r") as f:
        data = json.load(f)

    # check for new file format
    if "rims_scheme" in data.keys():
        data = data["rims_scheme"]

    return data
