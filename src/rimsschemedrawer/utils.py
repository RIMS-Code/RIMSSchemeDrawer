# Utility functions for the rims scheme drawer

from typing import Union

import matplotlib
import numpy as np

DEFAULT_SETTINGS = {
    "settings": {
        "plot_title": "",
        "fig_width": 5,
        "fig_height": 8,
        "fs_title": 14,
        "fs_axes": 11,
        "fs_axes_labels": 11,
        "fs_labels": 11,
        "headspace": 2500,
        "arrow_width": 0.2,
        "arrow_head_width": 0.6,
        "prec_wavelength": 3,
        "prec_level": 0,
        "line_breaks": True,
        "ip_label_pos": "Bottom",
        "show_forbidden_transitions": "x-out",
        "show_transition_strength": True,
        "show_cm-1_axis": True,
        "show_eV_axis": True,
        "plot_style": "light",
    },
    "scheme": {
        "gs_term": "",
        "ip_term": "",
        "last_step_to_ip": False,
    },
}

IP_DICTIONARY = {
    "H": 109678.77174307,
    "He": 198310.66637,
    "Li": 43487.1142,
    "Be": 75192.64,
    "B": 66928.04,
    "C": 90820.348,
    "N": 117225.7,
    "O": 109837.02,
    "F": 140524.5,
    "Ne": 173929.75,
    "Na": 41449.451,
    "Mg": 61671.05,
    "Al": 48278.48,
    "Si": 65747.76,
    "P": 84580.83,
    "S": 83559.1,
    "Cl": 104591.01,
    "Ar": 127109.842,
    "K": 35009.814,
    "Ca": 49305.924,
    "Sc": 52922.0,
    "Ti": 55072.5,
    "V": 54411.67,
    "Cr": 54575.6,
    "Mn": 59959.56,
    "Fe": 63737.704,
    "Co": 63564.6,
    "Ni": 61619.77,
    "Cu": 62317.46,
    "Zn": 75769.31,
    "Ga": 48387.634,
    "Ge": 63713.24,
    "As": 78950.0,
    "Se": 78658.15,
    "Br": 95284.8,
    "Kr": 112914.433,
    "Rb": 33690.81,
    "Sr": 45932.2036,
    "Y": 50145.6,
    "Zr": 53507.832,
    "Nb": 54513.8,
    "Mo": 57204.3,
    "Tc": 57421.68,
    "Ru": 59366.4,
    "Rh": 60160.1,
    "Pd": 67241.14,
    "Ag": 61106.45,
    "Cd": 72540.05,
    "In": 46670.107,
    "Sn": 59232.69,
    "Sb": 69431.34,
    "Te": 72669.006,
    "I": 84294.9,
    "Xe": 97833.787,
    "Cs": 31406.4677325,
    "Ba": 42034.91,
    "La": 44981.0,
    "Ce": 44672.0,
    "Pr": 44120.0,
    "Nd": 44562.0,
    "Pm": 45020.8,
    "Sm": 45519.69,
    "Eu": 45734.74,
    "Gd": 49601.45,
    "Tb": 47295.0,
    "Dy": 47901.76,
    "Ho": 48567.0,
    "Er": 49262.0,
    "Tm": 49880.57,
    "Yb": 50443.2,
    "Lu": 43762.6,
    "Hf": 55047.9,
    "Ta": 60891.4,
    "W": 63427.7,
    "Re": 63181.6,
    "Os": 68058.9,
    "Ir": 72323.9,
    "Pt": 72257.8,
    "Au": 74409.11,
    "Hg": 84184.15,
    "Tl": 49266.66,
    "Pb": 59819.558,
    "Bi": 58761.65,
    "Po": 67896.31,
    "At": 75150.8,
    "Rn": 86692.5,
    "Fr": 32848.872,
    "Ra": 42573.36,
    "Ac": 43394.52,
    "Th": 50867.0,
    "Pa": 49034.0,
    "U": 49958.4,
    "Np": 50535.0,
    "Pu": 48601.0,
    "Am": 48182.0,
    "Cm": 48330.68,
    "Bk": 49989.0,
    "Cf": 50666.76,
    "Es": 51364.58,
    "Fm": 52422.5,
    "Md": 53230.0,
    "No": 53444.0,
    "Lr": 40005.0,
    "Rf": 48580.0,
    "Db": 55000.0,
    "Sg": 63000.0,
    "Bh": 62000.0,
    "Hs": 61000.0,
}

IP_REFERENCES_NON_NIST = {
    "Pa": {
        "author": "Naubereit",
        "year": 2020,
        "url": "http://doi.org/10.25358/openscience-5183",
    },
    "Fm": {
        "author": "Grotrian",
        "year": 2024,
        "url": "http://grotrian.nsu.ru/en/element/54354",
    },
    "Md": {
        "author": "Grotrian",
        "year": 2024,
        "url": "http://grotrian.nsu.ru/en/element/54355",
    },
}

LASERS = ["Ti:Sa", "Dye", "Ti:Sa and Dye"]  # default is first entry - Ti:Sa

PLOT_STYLES = ["light", "dark", "light transparent", "dark transparent"]


def color_wavelength(lmb: float, darkmode: bool = False) -> str:
    """Color the wavelength according to the wavelength.

    When darkmode is turned on, pastel colors are used. Definitions of colors are
    taken from here:
    https://sciencenotes.org/visible-light-spectrum-wavelengths-and-colors/

    :param lmb: Wavelength in nm.

    :return: Color string.
    """
    dict_light = {
        "ir": "#500000",
        "red": "#b70000",
        "orange": "#d75700",
        "yellow": "#c09e00",
        "green": "#0aa000",
        "light_blue": "#0098ff",
        "deep_blue": "#0012a0",
        "violet": "#5f00a0",
    }
    dict_dark = {
        "ir": "#b98989",
        "red": "#d27878",
        "orange": "#ffa669",
        "yellow": "#f4e67c",
        "green": "#60a55b",
        "light_blue": "#82b1d1",
        "deep_blue": "#8c96df",
        "violet": "#9e85af",
    }

    if darkmode:
        dict_use = dict_dark
    else:
        dict_use = dict_light

    if lmb > 700:  # infrared
        return dict_use["ir"]
    elif lmb >= 625:  # red
        return dict_use["red"]
    elif lmb >= 590:  # orange
        return dict_use["orange"]
    elif lmb >= 565:  # yellow
        return dict_use["yellow"]
    elif lmb >= 500:  # green
        return dict_use["green"]
    elif lmb >= 484:  # light blue
        return dict_use["light_blue"]
    elif lmb >= 450:  # deep blue
        return dict_use["deep_blue"]
    else:  # violet
        return dict_use["violet"]


def cm_2_to_nm(cm: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert a wavenumber in cm^-1 to a wavelength in nm.

    :param cm: Wavenumber in cm^-1.
    :return: Wavelength in nm.
    """
    return 1e7 / cm


def get_elements() -> list:
    """Get a list of all elements."""
    return list(IP_DICTIONARY.keys())


def get_ip(ele: str) -> float:
    """Get the ionization potential for a given element.

    :param ele: Element symbol, not case sensitive.

    :return: Ionization potential in cm-1.
    """

    return IP_DICTIONARY[ele.capitalize()]


def get_ip_reference(ele: str) -> dict:
    """Get a reference for the ionization potential.

    If element is in `IP_REFERENCES_NON_NIST`, return the reference dictionary.
    Otherwise, return a dictionary with "NIST" entries.

    :return: Dictionary with "author", "year", and "url" entries.
    """
    nist_dict = {
        "author": "NIST ASD",
        "year": 2024,
        "url": "https://www.nist.gov/pml/atomic-spectra-database",
    }

    if ele in IP_REFERENCES_NON_NIST.keys():
        return IP_REFERENCES_NON_NIST[ele]
    else:
        return nist_dict


def guess_element_from_ip(ip: float) -> str:
    """Guess an element from the ionization potential.

    This routine is mainly provided for backwards compatibility with older
    RIMSSchemeDrawer instances, where the user used to define the IP manually.

    :param ip: Ionization potential in cm-1.
    :return: Element symbol (best guess).
    """
    eles, values = list(IP_DICTIONARY.keys()), list(IP_DICTIONARY.values())
    values = np.array(values)
    diff = np.abs(values - ip)
    ind = np.argmin(diff)
    return eles[ind]


def my_exp_formatter(val: float, prec: int) -> str:
    """Format a value with a given precision to LaTeX output."""
    value_str = f"{val:.{prec}e}"
    numb, exp = value_str.split("e")
    return f"${numb} \\times 10^{{{int(exp)}}}$"


def my_formatter(val: float, *args) -> str:
    """Format the axis labels for the left y-axis in scientific notation.

    :param val: Value to format, must be >= 0.
    :param args: Additional arguments - will be ignored.

    :return: Properly formatted string.
    """
    fform = matplotlib.ticker.ScalarFormatter(useOffset=False, useMathText=True)
    fform.set_scientific((0, 0))
    if val <= 1e-9:  # some reasonable cutoff
        val_ret = "$0$"
    else:
        val_ret = f"${fform.format_data(val)}$"

    return val_ret


def nm_to_cm_2(nm: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert a wavelength in nm to wavenumber in cm^-1.

    :param nm: Wavelength in nm.
    :return: Wavenumber in cm^-1.
    """
    return 1e7 / nm


def term_to_string(tstr: str):
    """Convert term symbol to LaTeX enabled string.

    Converts a term symbol string to a LaTeX enabled matplotlib string
    If already a LaTeX string, just return it.
    :param tstr:   Input string to convert
    :return:       Output string LaTeX enabled for Matplotlib
    """
    if tstr == "":
        return None

    latex_characters = ["{", "}", "^", "_"]
    for lch in latex_characters:
        if lch in tstr:
            tstr = tstr.replace(" ", "\\,")
            return f"${tstr}$"

    # some exceptionslike AI and IP
    if tstr == "IP":
        return "IP"
    if tstr == "AI":
        return "AI"
    if tstr == "Rydberg":
        return "Rydberg"
    if tstr == "Ryd":
        return "Ryd"

    # if there is an equal sign in there, leave it as is
    if tstr.find("=") != -1:
        return tstr

    # find the first slash and start looking for the letter after that
    start = tstr.find("/") + 1
    letterind = -1
    for it in range(start, len(tstr)):
        try:
            float(tstr[it])
        except ValueError:
            letterind = it
            break
    # if / comes after the letter:
    if letterind == -1:
        start = 0
        letterind = -1
        for it in range(start, len(tstr)):
            try:
                float(tstr[it])
            except ValueError:
                letterind = it
                break
    if letterind == -1:
        return tstr

    # set up the three parts for the latex string
    tmp1 = "$^{" + tstr[0:letterind] + "}$"
    tmp2 = tstr[letterind]
    tmp3 = "$_{" + tstr[letterind + 1 :] + "}$"

    return tmp1 + tmp2 + tmp3
