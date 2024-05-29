"""Module to parse the json file and return parameters."""

import json
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

try:
    from rttools import StringFmt
except ImportError:
    StringFmt = None

import rimsschemedrawer.utils as ut


class ConfigParser:
    """Class to parse the json configuration file.

    All levels and scheme configurations will be saved as numpy arrays.
    """

    def __init__(self, data: Dict):
        """Initialize the class by parsing the data and saving it as variables."""
        self._num_steps = None
        self.data = data
        self._element_guessed = False

        self._last_step_to_ip_mode = False

        self._parse_data_scheme()
        self._parse_data_settings()

    # SCHEME PROPERTIES

    @property
    def element(self) -> str:
        """Get the element of the scheme."""
        return self._element

    @property
    def element_guessed(self) -> bool:
        """Return if the element was guessed from the IP."""
        return self._element_guessed

    @property
    def gs_level(self) -> float:
        """Get the ground state level."""
        return self._gs_level

    @property
    def gs_term(self) -> str:
        """Get the ground state term, formatted for plotting."""
        return ut.term_to_string(self._gs_term)

    @property
    def gs_term_html(self):
        """Get the ground state term, formatted for HTML."""
        rttools_error()
        return StringFmt(self.gs_term, StringFmt.Type.latex).html

    @property
    def gs_term_no_formatting(self) -> str:
        """Get the ground state term, not formatted for plotting."""
        return self._gs_term

    @property
    def ip_level(self) -> float:
        """Get the ionization potential level."""
        return self._ip_level

    @property
    def ip_term(self) -> str:
        """Get the ionization potential term, formatted for plotting."""
        return ut.term_to_string(self._ip_term)

    @property
    def ip_term_no_formatting(self):
        """Get the ionization potential term, not formatted for plotting."""
        return self._ip_term

    @property
    def is_low_lying(self) -> np.ndarray:
        """Return a boolean array if a level is a low-lying state.

        This array has as many entries as there are steps in the scheme.

        :return: Boolean array if a level is a low-lying state.
        """
        return self._low_lying

    @property
    def lasers(self) -> str:
        """Get the types of lasers used in this scheme (defaults to Ti:Sa)."""
        return self._lasers

    @property
    def last_step_to_ip(self) -> bool:
        """Get the last step to the ionization potential setup in file."""
        return self._last_step_to_ip

    @property
    def last_step_to_ip_mode(self) -> bool:
        """Get if we are actually in last step to IP mode?"""
        return self._last_step_to_ip_mode

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
    def step_terms_html(self) -> np.ndarray:
        """Get the terms for all states, formatted for HTML."""
        rttools_error()
        return np.array(
            [StringFmt(it, StringFmt.Type.latex).html for it in self.step_terms]
        )

    @property
    def step_terms_no_formatting(self) -> np.ndarray:
        """Get the terms for all states, not formatted for plotting."""
        return self._step_term

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
        #
        return self._sett_line_breaks

    @property
    def sett_prec(self) -> Tuple[int, int]:
        """Get the precisions for the plot.

        :return: Precisions for: wavelength, level
        """
        return self._sett_prec

    @property
    def sett_plot_dark(self) -> bool:
        """Get the darkmode setting for the plot.

        :return: Darkmode setting.
        """
        return "dark" in self._sett_plot_style

    @property
    def sett_plot_style(self) -> str:
        """Get the plot style setting for the plot.

        :return: Plot style setting.
        """
        return self._sett_plot_style

    @property
    def sett_plot_transparent(self) -> bool:
        """Get the transparent setting for the plot.

        :return: Transparent setting.
        """
        return "transparent" in self._sett_plot_style

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

    @property
    def sett_unit_nm(self) -> bool:
        """Return if the unit is in nm."""
        return self._input_nm

    # METHODS

    def scheme_table(self, prec: int = 3, prec_strength: int = 1) -> Tuple[List, List]:
        """Create a scheme table for further processing.

        The headers are the following:
        - Step
        - λ (nm)
        - From (cm⁻¹)  - including term symbol formatted
        - To (cm⁻¹) - including term symbol formatted
        - Forbidden - filled in as "x" if forbidden (only if there are forbidden steps)
        - Strength (s⁻¹) - formatted as html string to given precision
            (only present if any transitions were given)

        Table: All entries are formatted as strings!

        :param prec: Precision for the wavelength and steps.
        :param prec_strength: Precision for the transition strength.

        :return: Tuple with headers and the scheme table.
        """
        rttools_error()

        def reshuffle_list_low_lying(lst: List) -> List:
            """Reshuffle a given list when low-lying states are present.

            Low-lying states are stored first, then the step from the ground state, and
            then the actual steps. This function reshuffles the list to have the step
            from the ground state first, then the low-lying states, and then the actual
            steps. If no low-lying states are present, do nothing.

            :param lst: List to reshuffle.
            """
            if np.any(self._low_lying):
                idx_first_step = np.where(~self._low_lying)[0][0]
                tmp_value = lst.pop(idx_first_step)
                lst.insert(0, tmp_value)
                return lst

            return lst

        headers = [
            "Step",
            "λ (nm)",
            "From (cm⁻¹)",
        ]

        has_from_term = any(self.step_terms) or self.gs_term
        has_to_term = any(self.step_terms) or self.ip_term
        if has_from_term:
            headers.append("Term")
        headers.append("To (cm⁻¹)")
        if has_to_term:
            headers.append("Term")

        first_no_lowlying = np.where(~self._low_lying)[0][0]

        steps = np.ones(self.number_of_levels, dtype=int)
        for it in range(first_no_lowlying + 1, len(steps)):
            steps[it] += steps[it - 1]

        lambdas = [f"{it:.{prec}f}" for it in self._steps_nm]
        lambdas = reshuffle_list_low_lying(lambdas)

        from_level = ["" for _ in range(self.number_of_levels)]
        from_term = from_level.copy()
        # add low-lying states
        for it in range(first_no_lowlying):
            tmp_str = f"{self.step_levels[it]:.{prec}f}"
            if term := self.step_terms_html[it]:
                from_term[it] = term
            from_level[it] = tmp_str
        # add ground state
        gs = self.gs_level
        if gs == 0:
            tmp_str = "0"
        else:
            tmp_str = f"{gs:.{prec}f}"
        from_level[first_no_lowlying] = tmp_str
        if term := self.gs_term_html:
            from_term[first_no_lowlying] = term
        # add steps
        for it in range(
            first_no_lowlying + 1, self.number_of_levels
        ):  # above ground state
            tmp_str = f"{self.step_levels[it - 1]:.{prec}f}"
            if term := self.step_terms_html[it - 1]:
                from_term[it] = term
            from_level[it] = tmp_str
        from_level = reshuffle_list_low_lying(from_level)
        from_term = reshuffle_list_low_lying(from_term)

        to_level = ["" for _ in range(self.number_of_levels)]
        to_term = to_level.copy()
        # add low-lying states and first step
        for it in range(first_no_lowlying + 1):
            tmp_str = f"{self.step_levels[first_no_lowlying]:.{prec}f}"
            if term := self.step_terms_html[first_no_lowlying]:
                to_term[it] = term
            to_level[it] = tmp_str
        # add steps
        for it in range(first_no_lowlying + 1, self.number_of_levels):
            tmp_str = f"{self.step_levels[it]:.{prec}f}"
            if term := self.step_terms_html[it]:
                to_term[it] = term
            to_level[it] = tmp_str
        to_level = reshuffle_list_low_lying(to_level)
        to_term = reshuffle_list_low_lying(to_term)

        # forbidden transitions
        if np.any(self.step_forbidden):
            headers.append("Forbidden")
            forbidden = ["x" if it else "" for it in self.step_forbidden]
            forbidden = reshuffle_list_low_lying(forbidden)

        # transition strength
        if np.any(self.transition_strengths):
            transition_strengths = []
            headers.append("Strength (s⁻¹)")
            for val in self.transition_strengths:
                if val != 0:
                    transition_strengths.append(
                        StringFmt(
                            ut.my_exp_formatter(val, prec_strength),
                            StringFmt.Type.latex,
                        ).html
                    )
                else:
                    transition_strengths.append("")
            transition_strengths = reshuffle_list_low_lying(transition_strengths)

        # create table
        table = []
        for idx in range(self.number_of_levels):
            row = [
                str(steps[idx]),
                lambdas[idx],
                from_level[idx],
            ]
            if has_from_term:
                row.append(from_term[idx])
            row.append(to_level[idx])
            if has_to_term:
                row.append(to_term[idx])
            if np.any(self.step_forbidden):
                row.append(forbidden[idx])
            if np.any(self.transition_strengths):
                row.append(transition_strengths[idx])
            table.append(row)

        return headers, table

    # PRIVATE METHODS

    def _parse_data_scheme(self):
        """Parse the data of the scheme and save it to class variables."""
        # variable that defines if input is in nm (True). Otherwise in cm^-1 (False)
        self._input_nm = True if self.data["scheme"]["unit"] == "nm" else False

        # ground state
        self._gs_level = float(self.data["scheme"]["gs_level"])
        self._gs_term = self.data["scheme"]["gs_term"]

        # IP
        try:  # new format with element instead of IP defined
            self._element = self.data["scheme"]["element"]
            self._ip_level = ut.get_ip(self._element)
        except KeyError:  # new format with element instead of IP defined
            self._ip_level = float(self.data["scheme"]["ip_level"])
            self._element = ut.guess_element_from_ip(self._ip_level)
            self._element_guessed = True
        self._ip_term = self.data["scheme"]["ip_term"]

        # Get the laser value and default to Ti:Sa if none selected
        try:
            self._lasers = self.data["scheme"]["laser"]
        except KeyError:
            self._lasers = ut.LASERS[0]

        # get last step to IP
        last_step_to_ip_default = ut.DEFAULT_SETTINGS["scheme"]["last_step_to_ip"]
        self._last_step_to_ip = self.data["scheme"].get(
            "last_step_to_ip", last_step_to_ip_default
        )

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

        # adjust scheme if last_step_to_ip and set mode if required
        if self._last_step_to_ip and self._step_levels_cm[-1] < self._ip_level:
            self._last_step_to_ip_mode = True
            # append the last step
            self._step_levels_cm = np.append(self._step_levels_cm, self._ip_level)
            self._steps_nm = np.append(
                self._steps_nm, ut.cm_2_to_nm(self._ip_level - self._step_levels_cm[-2])
            )
            self._forbidden = np.append(self._forbidden, False)
            self._low_lying = np.append(self._low_lying, False)
            self._transition_strength = np.append(self._transition_strength, 0)
            self._step_term = np.append(self._step_term, "")

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
            try:
                return dtype(self.data["settings"][key])
            except KeyError:
                return dtype(ut.DEFAULT_SETTINGS["settings"][key])

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
        self._sett_plot_style = get_value("plot_style", str)


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


def rttools_error():
    """Check for rttools and raise an error if not found."""
    if StringFmt is None:
        raise ImportError(
            "rttools is not installed. Please install it to use this function."
        )
