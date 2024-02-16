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
        "fs_axes": 12,
        "fs_axes_labels": 12,
        "fs_labels": 12,
        "headspace": 3000,
        "arrow_width": 0.2,
        "arrow_head_width": 0.6,
        "prec_wavelength": 3,
        "prec_level": 0,
        "line_breaks": False,
        "ip_label_pos": "Bottom",
        "show_forbidden_transitions": "x-out",
        "show_transition_strength": True,
        "show_cm-1_axis": True,
        "show_eV_axis": True,
        "plot_darkmode": False,
    },
    "scheme": {
        "gs_term": "",
        "ip_term": "",
    },
}


def cm_2_to_nm(cm: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Convert a wavenumber in cm^-1 to a wavelength in nm.

    :param cm: Wavenumber in cm^-1.
    :return: Wavelength in nm.
    """
    return 1e7 / cm


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
    """
    Converts a term symbol string to a LaTeX enabled matplotlib string
    :param tstr:   Input string to convert
    :return:       Output string LaTeX enabled for Matplotlib
    """
    if tstr == "":
        return None

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
