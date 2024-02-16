# Test utility functions for the project

from hypothesis import given, strategies as st
import pytest

from rimsschemedrawer import utils as ut


def test_cm_2_to_nm():
    """Check that the conversion from cm^-1 to nm is correct."""
    assert ut.cm_2_to_nm(1e7) == 1
    assert ut.cm_2_to_nm(5e6) == 2
    assert ut.cm_2_to_nm(3.3333333333333335e6) == 3


@pytest.mark.parametrize(
    "values",
    [
        [1.2345e6, 3, "$1.234 \\times 10^{6}$"],
        [0.001, 2, "$1.00 \\times 10^{-3}$"],
        [1, 1, "$1.0 \\times 10^{0}$"],
    ],
)
def test_my_exp_formatter(values):
    """Format exponential values as LaTeX strings."""
    value = values[0]
    prec = values[1]
    str_exp = values[2]

    str_ret = ut.my_exp_formatter(value, prec)

    assert str_ret == str_exp


@given(value=st.floats(min_value=0, allow_infinity=False))
def test_my_formatter(value):
    """Return properly formatted LaTeX code."""
    ret = ut.my_formatter(value)

    # LaTeX key elements
    assert ret[0] == "$"
    assert ret[-1] == "$"

    if value <= 1e-9:  # ensure scientific notation
        assert ret == "$0$"
    elif value >= 10:
        assert "^{" in ret
        assert ret[-2] == "}"


def test_nm_to_cm_2():
    """Check that the conversion from nm to cm^-1 is correct."""
    assert ut.nm_to_cm_2(1) == 1e7
    assert ut.nm_to_cm_2(2) == 5e6
    assert ut.nm_to_cm_2(3) == 3.3333333333333335e6


@pytest.mark.parametrize("vals", [["3F2", "$^{3}$F$_{2}$"], ["4G1", "$^{4}$G$_{1}$"]])
def test_term_to_string(vals):
    """Check that the term symbols are converted correctly."""
    assert ut.term_to_string(vals[0]) == vals[1]


@pytest.mark.parametrize("val", ["IP", "AI", "Rydberg", "Ryd"])
def test_term_to_string_no_change(val):
    """Leave these symbols / strings unchanged."""
    assert ut.term_to_string(val) == val
