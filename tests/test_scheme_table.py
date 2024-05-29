# Tests for ConfigParser scheme table creation.

from rttools import StringFmt

import rimsschemedrawer.json_parser as jp
from rimsschemedrawer.utils import term_to_string


def tts(term: str) -> str:
    """Convert to expected term."""
    ltx = term_to_string(term)
    return StringFmt(ltx, StringFmt.Type.latex).html


def test_ti_new_json(data_path):
    """Return the correct table for the new Ti scheme."""
    json_file = data_path.joinpath("ti_new.json")
    data = jp.json_reader(json_file)

    parser = jp.ConfigParser(data)

    header_exp = [
        "Step",
        "λ (nm)",
        "From (cm⁻¹)",
        "Term",
        "To (cm⁻¹)",
        "Term",
    ]

    table_exp = [
        ["1", "465.777", "0", f"{tts('3F2')}", "21469.500", f"{tts('3G3')}"],
        ["1", "469.498", "170.150", f"{tts('3F3')}", "21469.500", f"{tts('3G3')}"],
        ["1", "474.324", "386.880", f"{tts('3F4')}", "21469.500", f"{tts('3G3')}"],
        ["2", "416.158", "21469.500", f"{tts('3G3')}", "45498.850", f"{tts('3G4')}"],
        ["3", "881.399", "45498.850", f"{tts('3G4')}", "56844.450", ""],
    ]

    header, table = parser.scheme_table()

    assert header == header_exp
    assert table == table_exp


def test_raised_ground(data_path):
    """Return the correct table for a scheme with a raised ground level."""
    json_file = data_path.joinpath("raised_ground_cm.json")
    data = jp.json_reader(json_file)

    parser = jp.ConfigParser(data)

    header_exp = [
        "Step",
        "λ (nm)",
        "From (cm⁻¹)",
        "Term",
        "To (cm⁻¹)",
        "Term",
        "Forbidden",
        "Strength (s⁻¹)",
    ]

    table_exp = [
        [
            "1",
            "400.262",
            "1000.000",
            f"{tts('5D0')}",
            "25983.609",
            f"{tts('5F1')}",
            "",
            "1.0 × 10<sup>6</sup>",
        ],
        [
            "2",
            "407.469",
            "25983.609",
            f"{tts('5F1')}",
            "50525.354",
            f"{tts('5D2')}",
            "x",
            "",
        ],
        [
            "3",
            "771.908",
            "50525.354",
            f"{tts('5D2')}",
            "63480.266",
            f"{tts('AI')}",
            "",
            "3.0 × 10<sup>5</sup>",
        ],
    ]

    header, table = parser.scheme_table()

    assert header == header_exp
    assert table == table_exp
