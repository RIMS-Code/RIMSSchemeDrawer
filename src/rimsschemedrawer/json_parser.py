"""Module to parse the json file and return parameters."""

import json
from pathlib import Path
from typing import Dict, Tuple

import numpy as np

import rimsschemedrawer.utils as ut


class ConfigParser:
    """Class to parse the json configuration file.

    All levels and scheme configurations will be saved as numpy arrays.
    """

    def __init__(self, data: Dict):
        """Initialize the class by parsing the data and saving it as variables."""
        self._num_steps = None
        self.data = data

        self._parse_data_scheme()
        self._parse_data_settings()

    # SCHEME PROPERTIES

    @property
    def gs_level(self) -> float:
        """Get the ground state level."""
        return self._gs_level

    @property
    def gs_term(self) -> str:
        """Get the ground state term, formatted for plotting."""
        return ut.term_to_string(self._gs_term)

    @property
    def ip_level(self) -> float:
        """Get the ionization potential level."""
        return self._ip_level

    @property
    def ip_term(self) -> str:
        """Get the ionization potential term, formatted for plotting."""
        return ut.term_to_string(self._ip_term)

    @property
    def is_low_lying(self) -> np.ndarray:
        """Return a boolean array if a level is a low-lying state.

        This array has as many entries as there are steps in the scheme.

        :return: Boolean array if a level is a low-lying state.
        """
        return self._low_lying

    @property
    def number_of_levels(self) -> int:
        """Get the number of steps in the scheme."""
        return self._num_steps

    @property
    def step_levels(self) -> np.ndarray:
        """Get all levels of the scheme."""
        return self._step_levels_cm

    @property
    def step_forbidden(self) -> np.ndarray:
        """Get all forbidden transitions."""
        return self._forbidden

    @property
    def step_nm(self) -> np.ndarray:
        """Get the steps for all states in nm."""
        return self._steps_nm

    @property
    def step_terms(self) -> np.ndarray:
        """Get the terms for all states, formatted for plotting."""
        return np.array([ut.term_to_string(it) for it in self._step_term])

    @property
    def transition_strengths(self) -> np.ndarray:
        """Get the transition strength of all steps."""
        return self._transition_strength

    # SETTINGS PROPERTIES

    @property
    def sett_arrow_fmt(self) -> Tuple[float, float]:
        """Get the arrow formatting for the plot.

        :return: Arrow width, arrow head width.
        """
        return self._sett_arrow_fmt

    @property
    def sett_darkmode(self) -> bool:
        """Get the darkmode setting for the plot.

        :return: Darkmode setting.
        """
        return self._sett_darkmode

    @property
    def sett_fig_size(self) -> Tuple[float, float]:
        """Get the figure size for the plot.

        :return: Figure size: width, height
        """
        return self._sett_fig_size

    @property
    def sett_fontsize(self) -> Tuple[int, int, int, int]:
        """Get the font sizes for the plot.

        :return: Font sizes for: axes ticks, axes labels, in-plot labels, title
        """
        return self._sett_fontsize

    @property
    def sett_headspace(self) -> float:
        """Get the headspace for the plot."""
        return self._sett_headspace

    @property
    def sett_ip_label_pos(self) -> str:
        """Get the position of the IP label."""
        return self._sett_ip_label_pos

    @property
    def sett_line_breaks(self) -> bool:
        """Get the line breaks setting for the plot."""
        return self._sett_line_breaks

    @property
    def sett_prec(self) -> Tuple[int, int]:
        """Get the precisions for the plot.

        :return: Precisions for: wavelength, level
        """
        return self._sett_prec

    @property
    def sett_shows(self) -> Tuple[bool, bool, str, bool]:
        """Get the settings for the plot.

        :return: Settings for: cm-1 axis, eV axis, forbidden transitions, transition strength
        """
        return self._sett_shows

    @property
    def sett_title(self) -> str:
        """Get the title for the plot."""
        return self._sett_title

    def _parse_data_scheme(self):
        """Parse the data of the scheme and save it to class variables."""
        # variable that defines if input is in nm (True). Otherwise in cm^-1 (False)
        self._input_nm = True if self.data["scheme"]["unit"] == "nm" else False

        # ground state
        self._gs_level = float(self.data["scheme"]["gs_level"])
        self._gs_term = self.data["scheme"]["gs_term"]

        # IP
        self._ip_level = float(self.data["scheme"]["ip_level"])
        self._ip_term = self.data["scheme"]["ip_term"]

        # Get the step levels and save them as cm-1 (transform if in nm)
        step_levels = []
        idx = 0
        breaker = True
        while breaker:
            try:
                step_level = self.data["scheme"][f"step_level{idx}"]
                try:  # append step level as float, if Value error, we are done
                    step_levels.append(float(step_level))
                    idx += 1
                except ValueError:  # we are done since we encountered an empty string
                    breaker = False
            except KeyError:  # we ran out of step_level keys in the json file
                breaker = False
        step_levels = np.array(step_levels)

        # Number of steps to look for
        self._num_steps = len(step_levels)

        # Get the step terms
        self._step_term = self._parse_data_key("step_term", str, "")

        # Get bool array if a level is a low-lying level
        self._low_lying = self._parse_data_key("step_lowlying", bool, False)

        # Get bool array if a step is forbidden
        self._forbidden = self._parse_data_key("step_forbidden", bool, False)

        # Get the transition strength of a step, set to 0 if not found
        self._transition_strength = self._parse_data_key("trans_strength", float, 0)

        # Set the step levels in cm-1
        # transform to nm, but only for non-low-lying levels, those are already in cm-1!
        ll_mask = np.where(~self._low_lying)  # mask for low lying states
        idx_first_step = ll_mask[0][0]  # where the first step actually starts!
        if self._input_nm:
            step_levels[ll_mask] = ut.nm_to_cm_2(
                step_levels[ll_mask]
            )  # now all in cm-1

            for it in range(idx_first_step + 1, len(step_levels)):
                step_levels[it] += step_levels[it - 1]

            # add ground level
            step_levels[ll_mask] += self._gs_level

        self._step_levels_cm = step_levels

        # now create the steps in nm
        self._steps_nm = np.zeros_like(self._step_levels_cm)

        # low-level states
        self._steps_nm[self._low_lying] = ut.cm_2_to_nm(
            self._step_levels_cm[idx_first_step] - self._step_levels_cm[self._low_lying]
        )
        # step from ground state
        self._steps_nm[idx_first_step] = ut.cm_2_to_nm(
            self._step_levels_cm[idx_first_step] - self._gs_level
        )
        # actual steps from second on
        for it in range(idx_first_step + 1, len(self._steps_nm)):
            self._steps_nm[it] = ut.cm_2_to_nm(
                self._step_levels_cm[it] - self._step_levels_cm[it - 1]
            )

    def _parse_data_key(self, key: str, dtype: type, default: any) -> np.ndarray:
        """Parse a key from the data and return values with the correct type.

        All keys with `key{idx}`, where `idx` runs from 0 to `self._num_steps` will
        be parsed. If a key is not found, the default value will be entered in its
        place. Finally, a numpy array will be returned with the parsed values.
        If `self._num_steps` is not set, a ValueError will be raised.

        :param key: Key (first part without the number) to look for.
        :param dtype: Data type of the values -> will transform to this.
        :param default: Default value if key is not found.

        :return: Numpy array with the parsed values. Length: `self._num_steps`.

        :raises ValueError: If `self._num_steps` is not set.
        """
        values = []

        if self._num_steps is None:
            raise ValueError("Number of steps is not set.")

        for idx in range(self._num_steps):
            try:
                value = self.data["scheme"][f"{key}{idx}"]
                values.append(dtype(value))
            except (KeyError, ValueError):  # key not found, conversion failed
                values.append(default)

        return np.array(values)

    def _parse_data_settings(self):
        """Parse the data of the settings and save it to class variables.

        All values - if not available - will be set to the default values defined in
        `utils.py`.
        """

        def get_value(key: str, dtype: type) -> any:
            """Get a value from the "settings" tab in the json file, or default.

            Gets a value, and if no value is defined in the json file, the default
            value from `utils.py` is returned.

            :param key: Key to look for in the json file.
            :param dtype: Data type of the value.

            :return: Value from the json file or default value.
            """
            return dtype(
                self.data["settings"].get(key, ut.DEFAULT_SETTINGS["settings"][key])
            )

        # Plot title
        self._sett_title = get_value("plot_title", str)

        # Figure size: width, height
        self._sett_fig_size = (
            get_value("fig_width", float),
            get_value("fig_height", float),
        )

        # Arrow formatting: Arrow width, arrow head width
        self._sett_arrow_fmt = (
            get_value("arrow_width", float),
            get_value("arrow_head_width", float),
        )

        # Font sizes: Axes ticks, axes labels, in-plot labels, title
        self._sett_fontsize = (
            get_value("fs_axes", float),
            get_value("fs_axes_labels", float),
            get_value("fs_labels", float),
            get_value("fs_title", float),
        )

        # Headspace
        self._sett_headspace = get_value("headspace", float)

        # IP label position
        self._sett_ip_label_pos = get_value("ip_label_pos", str)

        # Line breaks
        self._sett_line_breaks = get_value("line_breaks", bool)

        # Precisions: wavelength, level
        self._sett_prec = (
            get_value("prec_wavelength", int),
            get_value("prec_level", int),
        )

        # Shows: cm-1 axis, ev_axis, forbidden_transitions, transition_strength
        self._sett_shows = (
            get_value("show_cm-1_axis", bool),
            get_value("show_eV_axis", bool),
            get_value("show_forbidden_transitions", str),
            get_value("show_transition_strength", bool),
        )

        # Darkmode
        self._sett_darkmode = get_value("plot_darkmode", bool)


def json_reader(fin: Path) -> Dict:
    """Read a json file and return a dictionary.

    This can take old or new files and return the data that
    can be read by the program.

    :return: Dictionary with parameters for drawing the scheme.
    """
    with open(fin) as f:
        data = json.load(f)

    # check for new file format
    if "rims_scheme" in data.keys():
        data = data["rims_scheme"]

    return data
