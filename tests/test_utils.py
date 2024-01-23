# Test utility functions for the project

import json

from rimsschemedrawer import utils as ut


def test_json_reader(data_path):
    """Check that a valid json file is returned."""
    fin = data_path.joinpath("ti.json")
    data = ut.json_reader(fin)

    assert isinstance(data, dict)
    assert "scheme" in data.keys()
    assert "settings" in data.keys()


def test_json_reader_new(data_path, tmp_path):
    """Check correct output with new json format."""
    # todo: replace this construction with an actual new file
    fin = data_path.joinpath("ti.json")
    data = ut.json_reader(fin)
    data_new = {"rims_scheme": data}
    fin_new = tmp_path.joinpath("ti_new.json")
    with open(fin_new, "w") as f:
        json.dump(data_new, f)

    data_in = ut.json_reader(fin_new)
    assert isinstance(data_in, dict)
    assert "scheme" in data_in.keys()
    assert "settings" in data_in.keys()
