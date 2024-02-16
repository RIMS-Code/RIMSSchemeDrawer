# Test the plotter
import rimsschemedrawer.json_parser
from rimsschemedrawer.plotter import Plotter


def test_plotter(data_path, tmp_path):
    """Run through the plotter with a simple scheme, assert no errors."""
    fin = data_path.joinpath("ti.json")
    data = rimsschemedrawer.json_parser.json_reader(fin)

    fname = tmp_path.joinpath("test.pdf")
    fig = Plotter(data)
    fig.savefig(fname)

    assert fname.exists()
