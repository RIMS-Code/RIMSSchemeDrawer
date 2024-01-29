"""Plotting functions and class for the rims scheme drawer."""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from rimsschemedrawer import utils as ut


class Plotter:
    def __init__(self, data: dict, saveplt=None, **kwargs):
        """Initialize the plotting class.

        :param data: Dictionary with the data to plot, directly from json file.
        :param saveplt: Name to save the plot to.
        :param kwargs: Additional keyword arguments.
            - number_of_steps: How many scheme steps to consider, default is 7.
                This number can be higher than the number of available steps!
        """
        self.data = data
        self.saveplt = saveplt

        # set kwargs
        self.number_of_steps = kwargs.get("number_of_steps", 7)

        # matplotlib parameters
        # tick size
        fsz_axes = int(data["settings"].get("fs_axes", 12))
        matplotlib.rc("xtick", labelsize=fsz_axes, direction="in")
        matplotlib.rc("ytick", labelsize=fsz_axes, direction="in")

        # figure stuff
        # self.canvas = FigureCanvas(self.figure)
        self.figure, self.axes = plt.subplots(1, 1)

        # Colors for arrows
        self.colir = "#a00000"
        self.coluv = "#0012a0"
        self.colfuv = "#5f00a0"
        self.colpump = "#0aa000"

        # fixme: remove this comment
        # figure size is not working properly with matplotlib argument. so let's force it by setting a fixed
        # central widget size - some temporary crap but works on mac osx. but does it work on windows? and linux?
        # test w/ different displays...?
        self.figwidth = float(data["settings"]["fig_width"])
        self.figheight = float(data["settings"]["fig_height"])

        # now plot the scheme
        self.plotit()

    def plotit(self):
        # textpad
        textpad = 0.4
        # percentage to increase for manifold
        mfld_yinc = 0.04  # in # of ipvalue
        #
        firstarrowxmfl = 1.0

        # gett settings from program

        fsz_title = int(self.data["settings"].get("fs_title", 14))
        fsz_axes_labels = int(self.data["settings"].get("fs_axes_labels", 14))
        fsz_labels = int(self.data["settings"].get("fs_labels", 12))
        sett_headspace = float(self.data["settings"].get("headspace", 2700))
        sett_arr = float(self.data["settings"].get("arrow_width", 0.2))
        sett_arr_head = float(self.data["settings"].get("arrow_head_width", 0.6))
        prec_lambda = int(self.data["settings"].get("prec_wavelength", 3))
        prec_level = int(self.data["settings"].get("prec_level", 0))

        # let's first get the wavelengths that we want and a list of bools if states are forbidden
        lambdas = []
        forbidden = []

        for it in range(self.number_of_steps):  # fixme; change number of steps here!
            try:
                lambdas.append(float(self.data["scheme"][f"step_level{it}"]))
                try:  # not all schemes have a forbidden step!
                    forbidden.append(self.data["scheme"][f"step_forbidden{it}"])
                except KeyError:
                    continue
            except KeyError:
                break

        # now only add lambdas that are NOT low lying states, same for forbidden steps!
        lambda_steps = []
        forbidden_steps = []
        for it in range(self.number_of_steps):
            try:
                if not self.data["scheme"][f"step_lowlying{it}"]:
                    lambda_steps.append(lambdas[it])
                    try:
                        forbidden_steps.append(forbidden[it])
                    except IndexError:
                        forbidden_steps.append(False)
            except KeyError:
                break

        # get the term symbols that were entered
        term_symb_entered = []
        for it in range(self.number_of_steps):
            try:
                if not self.data["scheme"][f"step_lowlying{it}"]:
                    term_symb_entered.append(self.data["scheme"][f"step_term{it}"])
            except KeyError:
                break

        # get ground state wavenumber
        wavenumber_gs = float(self.data["scheme"].get("gs_level", 0.0))

        # now go through the lambda steps and transform into actual wavelengths if not already
        unit = self.data["scheme"]["unit"]
        if unit != "nm":
            lambda_steps_temp = []
            for it in range(len(lambda_steps)):
                if lambda_steps[it] != "":
                    if it == 0:
                        lambda_steps_temp.append(
                            1.0e7 / (float(lambda_steps[it]) - float(wavenumber_gs))
                        )
                    else:
                        lambda_steps_temp.append(
                            1.0e7
                            / (float(lambda_steps[it]) - float(lambda_steps[it - 1]))
                        )
            # write lambda_steps back
            lambda_steps = list(lambda_steps_temp)

        # make lambda_steps into an np.array
        tmp = []
        for it in lambda_steps:
            try:
                tmp.append(float(it))
            except ValueError:
                break
        lambda_steps = np.array(tmp)

        # get more ground states if available (and forbidden states)
        wavenumber_es = []
        term_symb_es = []
        forbidden_es = []
        for it in range(self.number_of_steps):
            try:
                if self.data["scheme"][f"step_lowlying{it}"]:
                    wavenumber_es.append(float(self.data["scheme"][f"step_level{it}"]))
                    term_symb_es.append(self.data["scheme"][f"step_term{it}"])
                    try:
                        forbidden_es.append(self.data["scheme"][f"step_forbidden{it}"])
                    except KeyError:
                        forbidden_es.append(False)
            except KeyError:
                break

        # create wavenumber array
        wavenumber_steps = 1.0 / lambda_steps * 1e7

        transition_steps = np.zeros(len(wavenumber_steps))
        transition_steps[0] = wavenumber_steps[0] + wavenumber_gs
        for it in range(1, len(transition_steps)):
            transition_steps[it] = transition_steps[it - 1] + wavenumber_steps[it]

        # calculate total excitation in wavenumbers - for scaling later
        totwavenumber_photons = np.sum(wavenumber_steps)

        # get the ipvalue
        ipvalue = float(self.data["scheme"]["ip_level"])

        # ymax:
        if ipvalue > totwavenumber_photons + wavenumber_gs:
            ymax = ipvalue + sett_headspace
        elif totwavenumber_photons + wavenumber_gs - ipvalue < sett_headspace:
            ymax = ipvalue + sett_headspace
        else:
            ymax = totwavenumber_photons + wavenumber_gs

        # create term symbol string for direct usage in plotting
        term_symb = []
        term_symb_es_formatted = []
        for it in range(len(wavenumber_steps)):
            term_symb.append(ut.term_to_string(term_symb_entered[it]))
        for it in range(len(term_symb_es)):
            term_symb_es_formatted.append(ut.term_to_string(term_symb_es[it]))
        # get term symbol for ip and gs
        term_symb_ip = ut.term_to_string(self.data["scheme"].get("ip_term", ""))
        term_symb_gs = ut.term_to_string(self.data["scheme"].get("gs_term", ""))

        # break line or put in comma, depending on option
        lbreak = ", "
        if self.data["settings"].get("line_breaks", False):
            lbreak = "\n"

        # ### CREATE FIGURE ###
        # seocnd axes -> mirror of first
        a2 = self.axes.twinx()

        # figure width and height)
        figwidth = self.figwidth
        figheight = self.figheight
        self.figure.set_size_inches(figwidth, figheight, forward=True)

        # shade the level above the IP
        xshade = [0.0, 10.0]
        # the * 10. takes care if the user manually extends the range... to a certain degree at least, i.e., ymax*10
        self.axes.fill_between(
            xshade, ipvalue, ymax * 10.0, facecolor="#adbbff", alpha=0.5
        )
        # label the IP
        if self.data["settings"].get("ip_label_pos", "Top") == "Top":
            iplabelypos = ipvalue + 0.01 * totwavenumber_photons
            iplabelyalign = "bottom"
        else:
            iplabelypos = ipvalue - 0.01 * totwavenumber_photons
            iplabelyalign = "top"
        if term_symb_ip is None:
            iplabelstr = "IP, %.*f" % (int(prec_level), ipvalue) + "$\,$cm$^{-1}$"
        else:
            iplabelstr = (
                "IP, %.*f" % (int(prec_level), ipvalue)
                + "$\,$cm$^{-1}$"
                + lbreak
                + term_symb_ip
            )
        # ip above or below
        self.axes.text(
            textpad,
            iplabelypos,
            iplabelstr,
            color="k",
            ha="left",
            va=iplabelyalign,
            size=fsz_labels,
        )

        # Draw the horizontal lines for every transition and IP, unless transition is above IP (shade area there)
        for it in transition_steps:
            if it < ipvalue:
                self.axes.hlines(it, xmin=0, xmax=10, color="k")
        # Lines for manifold groundstater
        for it in range(len(wavenumber_es)):
            self.axes.hlines(
                mfld_yinc * ipvalue * (1 + it),
                xmin=1.5 * it + 2.3,
                xmax=1.5 * it + 3.7,
                linestyle="solid",
                color="k",
            )

        # Draw the horizontal lines for every transition and IP, unless transition is above IP (shade area there)
        for it in transition_steps:
            if it < ipvalue:
                self.axes.hlines(it, xmin=0, xmax=10, color="k")

        # draw the state we come out of, if not ground state
        if float(wavenumber_gs) > 0.0:
            self.axes.hlines(float(wavenumber_gs), xmin=0, xmax=10, color="k")

        # draw the arrows and cross them out if forbidden
        deltax = 8.65 / (len(lambda_steps) + 1.0) - 0.5
        xval = 0.0
        yval_bott = float(wavenumber_gs)
        # put in bottom level
        if term_symb_gs is None:
            levelstr = "%.*f" % (int(prec_level), wavenumber_gs) + "$\,$cm$^{-1}$"
        else:
            levelstr = (
                "%.*f" % (int(prec_level), wavenumber_gs)
                + "$\,$cm$^{-1}$"
                + lbreak
                + term_symb_gs
            )
        self.axes.text(
            10.0 - textpad,
            float(wavenumber_gs),
            levelstr,
            color="k",
            ha="right",
            va="bottom",
            size=fsz_labels,
        )

        for it in range(len(lambda_steps)):
            if lambda_steps[it] >= 700:
                col = self.colir
            elif 500.0 < lambda_steps[it] < 700.0:
                col = self.colpump
            elif 350.0 < lambda_steps[it] <= 500.0:
                col = self.coluv
            else:
                col = self.colfuv
            # xvalue for arrow
            xval += deltax
            wstp = wavenumber_steps[it]
            tstp = transition_steps[it]
            # check if transition is forbidden and no show is activated for the arrow
            if (
                not forbidden_steps[it]
                # fixme this is not in current gui, saved to json!
                or not self.data["settings"].get("show_arrows_forbidden", True)
            ):
                # look for where to plot the array
                xvalplot = 0.0
                if it == 0 and len(wavenumber_es) > 0:
                    xvalplot = firstarrowxmfl
                else:
                    xvalplot = xval
                # now plot the arrow
                self.axes.arrow(
                    xvalplot,
                    yval_bott,
                    0,
                    wstp,
                    width=sett_arr,
                    fc=col,
                    ec=col,
                    length_includes_head=True,
                    head_width=sett_arr_head,
                    head_length=totwavenumber_photons / 30.0,
                )

                # so we don't want to leave the arrow away but it is forbidden: then x it out!
                if forbidden_steps[it]:
                    yval_cross = yval_bott + wstp / 2.0
                    self.axes.plot(
                        xvalplot,
                        yval_cross,
                        "x",
                        color="r",
                        markersize=20,
                        markeredgewidth=5.0,
                    )

            # draw a little dashed line for the last one, AI and Rydberg state, to distinguish it from IP
            if it == len(lambda_steps) - 1:
                self.axes.hlines(
                    tstp, xmin=xval - 0.5, xmax=xval + 0.5, linestyle="solid", color="k"
                )

            # alignment of labels
            if xval <= 5.0:
                halignlam = "left"
                xloc_lambda = xval + textpad
                halignlev = "right"
                xloc_levelstr = 10.0 - textpad
            else:
                halignlam = "right"
                xloc_lambda = xval - textpad
                halignlev = "left"
                xloc_levelstr = textpad

            if (
                not forbidden_steps[it]
                or not self.parent.rbtn_sett_nodisparrow.isChecked()
            ):
                # wavelength text
                lambdastr = "%.*f" % (int(prec_lambda), lambda_steps[it]) + "$\,$nm"
                if it == 0 and len(wavenumber_es) > 0:
                    self.axes.text(
                        firstarrowxmfl + textpad,
                        tstp - wstp / 2.0,
                        lambdastr,
                        color=col,
                        ha=halignlam,
                        va="center",
                        rotation=90,
                        size=fsz_labels,
                    )
                else:
                    self.axes.text(
                        xval + textpad,
                        tstp - wstp / 2.0,
                        lambdastr,
                        color=col,
                        ha=halignlam,
                        va="center",
                        rotation=90,
                        size=fsz_labels,
                    )

            # level text
            if term_symb[it] is None:
                levelstr = "%.*f" % (int(prec_level), tstp) + "$\,$cm$^{-1}$"
            else:
                levelstr = (
                    "%.*f" % (int(prec_level), tstp)
                    + "$\,$cm$^{-1}$"
                    + lbreak
                    + term_symb[it]
                )
            if it == len(lambda_steps) - 1:
                leveltextypos = tstp
                leveltextvaalign = "center"
            else:
                leveltextypos = tstp - 0.01 * totwavenumber_photons
                leveltextvaalign = "top"
            self.axes.text(
                xloc_levelstr,
                leveltextypos,
                levelstr,
                color="k",
                ha=halignlev,
                va=leveltextvaalign,
                size=fsz_labels,
            )

            # update yval_bott
            yval_bott = transition_steps[it]

        # create ground state lambda step array
        lambda_step_es = []
        for it in range(len(wavenumber_es)):
            lambda_step_es.append(
                1.0e7
                / (
                    1.0e7 / lambda_steps[0]
                    - (float(wavenumber_es[it]) - float(wavenumber_gs))
                )
            )

        # now go through low lying excited states
        for it in range(len(wavenumber_es)):
            if lambda_step_es[it] >= 700:
                col = self.colir
            elif 500.0 < lambda_step_es[it] < 700.0:
                col = self.colpump
            elif 350.0 < lambda_step_es[it] <= 500.0:
                col = self.coluv
            else:
                col = self.colfuv

            # values
            xval = firstarrowxmfl + 1.5 + it * 1.5
            yval = mfld_yinc * ipvalue * (1 + it)
            wstp = float(wavenumber_steps[0]) - yval

            if not forbidden_es[it] or not self.data["settings"].get(
                "show_arrows_forbidden", True
            ):
                # xvalue for arrow
                self.axes.arrow(
                    xval,
                    yval,
                    0,
                    wstp,
                    width=sett_arr,
                    fc=col,
                    ec=col,
                    length_includes_head=True,
                    head_width=sett_arr_head,
                    head_length=totwavenumber_photons / 30.0,
                )

                # print cross out if necessary
                if forbidden_es[it]:
                    yval_cross = yval + wstp / 2.0
                    self.axes.plot(
                        xval,
                        yval_cross,
                        "x",
                        color="r",
                        markersize=20,
                        markeredgewidth=5.0,
                    )

                # wavelength text
                lambdastr = "%.*f" % (int(prec_lambda), lambda_step_es[it]) + "$\,$nm"
                self.axes.text(
                    xval + textpad,
                    yval + wstp / 2.0,
                    lambdastr,
                    color=col,
                    ha="left",
                    va="center",
                    rotation=90,
                    size=fsz_labels,
                )

            # level text
            if term_symb_es_formatted[it] is None:
                levelstr = (
                    "%.*f" % (int(prec_level), float(wavenumber_es[it]))
                    + "$\,$cm$^{-1}$"
                )
            else:
                # NO LINEBREAK HERE ON THESE LINES!
                levelstr = (
                    "%.*f" % (int(prec_level), float(wavenumber_es[it]))
                    + "$\,$cm$^{-1}$, "
                    + term_symb_es_formatted[it]
                )
            self.axes.text(
                xval + 0.5,
                yval,
                levelstr,
                color="k",
                ha="left",
                va="bottom",
                size=fsz_labels,
            )

        # Title:
        title_entry = self.data["settings"].get("plot_title", "")
        if title_entry != "":
            self.axes.set_title(title_entry, size=fsz_title)

        # ylabel
        self.axes.yaxis.set_major_formatter(ut.my_formatter)  # scientific labels
        if self.data["settings"].get("show_cm-1_axis", True):
            self.axes.set_ylabel("Wavenumber (cm$^{-1}$)", size=fsz_axes_labels)
        else:
            self.axes.axes.get_yaxis().set_ticks([])

        # axis limits
        self.axes.set_xlim([0.0, 10.0])
        self.axes.set_ylim([0.0, ymax])

        # eV axis on the right
        if self.data["settings"].get("show_eV_axis", True):
            a2.set_ylabel("Energy (eV)", size=fsz_axes_labels)
        else:
            a2.axes.get_yaxis().set_ticks([])
        a2.set_ylim([0.0, ymax / 8065.54429])

        # remove x ticks
        self.axes.axes.get_xaxis().set_ticks([])

        # tight layout of figure
        self.figure.tight_layout()

        if self.saveplt is not None:
            self.figure.savefig(self.saveplt)
