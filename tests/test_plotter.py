# Test the plotter

from rimsschemedrawer.plotter import Plotter
from rimsschemedrawer import utils as ut


def test_plotter(data_path, tmp_path):
    """Run through the plotter with a simple scheme, assert no errors."""
    fin = data_path.joinpath("ti.json")
    data = ut.json_reader(fin)

    fname = tmp_path.joinpath("test.pdf")
    fig = Plotter(data)
    fig.savefig(fname)

    assert fname.exists()
