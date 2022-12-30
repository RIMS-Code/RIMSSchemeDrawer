"""
Copyright (C) 2020-2021 Reto Trappitsch

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QFileDialog

import numpy as np
from os.path import expanduser

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# plotter - the heart of the whole thing
class Plotter(QMainWindow):
    def __init__(self, parent, saveplt=False):
        # initalize super
        super(Plotter, self).__init__(parent)
        self.parent = parent
        self.saveplt = saveplt

        # initialize the widget
        self.title = 'RIMS scheme'

        # matplotlib parameters
        # tick size
        fsz_axes = int(self.parent.edt_sett_fsaxes.text())
        matplotlib.rc('xtick', labelsize=fsz_axes, direction='in')
        matplotlib.rc('ytick', labelsize=fsz_axes, direction='in')

        # figure stuff
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)

        # add the figure toolbar to the main window
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.addToolBar(self.toolbar)

        # main widget
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.main_widget.setLayout(layout)

        # Colors for arrows
        self.colir = '#a00000'
        self.coluv = '#0012a0'
        self.colfuv = '#5f00a0'
        self.colpump = '#0aa000'

        # figure size is not working properly with matplotlib argument. so let's force it by setting a fixed
        # central widget size - some temporary crap but works on mac osx. but does it work on windows? and linux?
        # test w/ different displays...?
        figwidth = float(self.parent.edt_sett_figwidth.text())
        figheight = float(self.parent.edt_sett_figheight.text())
        self.centralWidget().setFixedWidth(int(figwidth * 100 + 24))
        self.centralWidget().setFixedHeight(int(figheight * 100 + 24))

        # now plot the scheme
        self.plotit()

    def plotit(self):
        # textpad
        textpad = 0.4
        # percentage to increase for manifold
        mfld_yinc = 0.04   # in # of ipvalue
        #
        firstarrowxmfl = 1.

        # gett settings from program
        # font sizes
        fsz_title = int(self.parent.edt_sett_fstitle.text())
        fsz_axes_labels = int(self.parent.edt_sett_fsaxlbl.text())
        fsz_labels = int(self.parent.edt_sett_fslbl.text())
        sett_headspace = float(self.parent.edt_sett_headspace.text())
        sett_arr = float(self.parent.edt_sett_arrwidth.text())
        sett_arr_head = float(self.parent.edt_sett_arrheadwidth.text())
        prec_lambda = int(self.parent.edt_sett_preclambda.text())
        prec_level = int(self.parent.edt_sett_preclevel.text())

        # let's first get the wavelengths that we want and a list of bools if states are forbidden
        lambdas = []
        forbidden = []
        for it in range(self.parent.numberofsteps):
            lambdas.append(self.parent.edt_level[it].text())
            forbidden.append(self.parent.chk_forbidden[it].isChecked())

        # now only add lambdas that are NOT low lying states, same for forbidden steps!
        lambda_steps = []
        forbidden_steps = []
        for it in range(self.parent.numberofsteps):
            if not self.parent.chk_lowlying[it].isChecked():
                lambda_steps.append(lambdas[it])
                forbidden_steps.append(forbidden[it])

        # get the term symbols that were entered
        term_symb_entered = []
        for it in range(self.parent.numberofsteps):
            if not self.parent.chk_lowlying[it].isChecked():
                term_symb_entered.append(self.parent.edt_term[it].text())

        # get ground state wavenumber
        if self.parent.edt_gslevel.text() is '':
            wavenumber_gs = 0.
        else:
            wavenumber_gs = float(self.parent.edt_gslevel.text())

        # now go through the lambda steps and transform into actual wavelengths if not already
        if self.parent.get_unit() is not 'nm':
            lambda_steps_temp = []
            for it in range(len(lambda_steps)):
                if lambda_steps[it] != '':
                    if it == 0:
                        lambda_steps_temp.append(1.e7 / (float(lambda_steps[it]) - float(wavenumber_gs)))
                    else:
                        lambda_steps_temp.append(1.e7 / (float(lambda_steps[it]) - float(lambda_steps[it-1])))
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
        for it in range(self.parent.numberofsteps):
            if self.parent.chk_lowlying[it].isChecked():
                wavenumber_es.append(float(self.parent.edt_level[it].text()))
                term_symb_es.append(self.parent.edt_term[it].text())
                forbidden_es.append(self.parent.chk_forbidden[it].isChecked())

        # create wavenumber array
        wavenumber_steps = 1. / lambda_steps * 1e7

        transition_steps = np.zeros(len(wavenumber_steps))
        transition_steps[0] = wavenumber_steps[0] + wavenumber_gs
        for it in range(1, len(transition_steps)):
            transition_steps[it] = transition_steps[it-1] + wavenumber_steps[it]

        # calculate total excitation in wavenumbers - for scaling later
        totwavenumber_photons = np.sum(wavenumber_steps)

        # get the ipvalue
        ipvalue = float(self.parent.edt_iplevel.text())

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
            term_symb.append(term_to_string(term_symb_entered[it]))
        for it in range(len(term_symb_es)):
            term_symb_es_formatted.append(term_to_string(term_symb_es[it]))
        # get term symbol for ip and gs
        term_symb_ip = term_to_string(self.parent.edt_ipterm.text())
        term_symb_gs = term_to_string(self.parent.edt_gsterm.text())

        # break line or put in comma, depending on option
        lbreak = ', '
        if self.parent.chk_sett_linebreaks.isChecked():
            lbreak = '\n'

        # ### CREATE FIGURE ###
        # seocnd axes -> mirror of first
        a2 = self.axes.twinx()

        # figure width and height)
        figwidth = float(self.parent.edt_sett_figwidth.text())
        figheight = float(self.parent.edt_sett_figheight.text())
        self.figure.set_size_inches(figwidth, figheight, forward=True)

        # tick label in scientific notation
        # a.ticklabel_format(style='sci', scilimits=(-3, 3), axis='both')
        fform = matplotlib.ticker.ScalarFormatter(useOffset=False, useMathText=True)
        gform = lambda x, pos: "${}$".format(fform._formatSciNotation('%1.10e' % x))
        self.axes.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(gform))
        a2.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(gform))

        # shade the level above the IP
        xshade = [0., 10.]
        # the * 10. takes care if the user manually extends the range... to a certain degree at least, i.e., ymax*10
        self.axes.fill_between(xshade, ipvalue, ymax*10., facecolor='#adbbff', alpha=0.5)
        # label the IP
        if self.parent.rbtn_iplable_top.isChecked():
            iplabelypos = ipvalue + 0.01*totwavenumber_photons
            iplabelyalign = 'bottom'
        else:
            iplabelypos = ipvalue - 0.01 * totwavenumber_photons
            iplabelyalign = 'top'
        if term_symb_ip is None:
            iplabelstr = 'IP, %.*f' %(int(prec_level), ipvalue) + '$\,$cm$^{-1}$'
        else:
            iplabelstr = 'IP, %.*f' %(int(prec_level), ipvalue) + '$\,$cm$^{-1}$' + lbreak + term_symb_ip
        # ip above or below
        self.axes.text(textpad, iplabelypos, iplabelstr, color='k', ha='left', va=iplabelyalign, size=fsz_labels)

        # Draw the horizontal lines for every transition and IP, unless transition is above IP (shade area there)
        for it in transition_steps:
            if it < ipvalue:
                self.axes.hlines(it, xmin=0, xmax=10, color="k")
        # Lines for manifold groundstater
        for it in range(len(wavenumber_es)):
            self.axes.hlines(mfld_yinc*ipvalue*(1+it), xmin=1.5*it+2.3, xmax=1.5*it+3.7,
                     linestyle='solid', color="k")

        # Draw the horizontal lines for every transition and IP, unless transition is above IP (shade area there)
        for it in transition_steps:
            if it < ipvalue:
                self.axes.hlines(it, xmin=0, xmax=10, color="k")

        # draw the state we come out of, if not ground state
        if float(wavenumber_gs) > 0.:
            self.axes.hlines(float(wavenumber_gs), xmin=0, xmax=10, color="k")

        # draw the arrows and cross them out if forbidden
        deltax = 8.65 / (len(lambda_steps) + 1.) - 0.5
        xval = 0.
        yval_bott = float(wavenumber_gs)
        # put in bottom level
        if term_symb_gs is None:
            levelstr = '%.*f' %(int(prec_level), wavenumber_gs) + '$\,$cm$^{-1}$'
        else:
            levelstr = '%.*f' %(int(prec_level), wavenumber_gs) + '$\,$cm$^{-1}$' + lbreak + term_symb_gs
        self.axes.text(10. - textpad, float(wavenumber_gs), levelstr, color='k', ha='right',
                       va='bottom', size=fsz_labels)

        for it in range(len(lambda_steps)):
            if lambda_steps[it] >= 700:
                col = self.colir
            elif 500. < lambda_steps[it] < 700.:
                col = self.colpump
            elif 350. < lambda_steps[it] <= 500.:
                col = self.coluv
            else:
                col = self.colfuv
            # xvalue for arrow
            xval += deltax
            wstp = wavenumber_steps[it]
            tstp = transition_steps[it]
            # check if transition is forbidden and no show is activated for the arrow
            if not forbidden_steps[it] or not self.parent.rbtn_sett_nodisparrow.isChecked():
                # look for where to plot the array
                xvalplot = 0.
                if it == 0 and len(wavenumber_es) > 0:
                    xvalplot = firstarrowxmfl
                else:
                    xvalplot = xval
                # now plot the arrow
                self.axes.arrow(xvalplot, yval_bott, 0, wstp, width=sett_arr, fc=col, ec=col, length_includes_head=True,
                                head_width=sett_arr_head, head_length=totwavenumber_photons/30.)

                # so we don't want to leave the arrow away but it is forbidden: then x it out!
                if forbidden_steps[it]:
                    yval_cross = yval_bott + wstp / 2.
                    self.axes.plot(xvalplot, yval_cross, 'x', color='r', markersize=20,
                                   markeredgewidth=5.)

            # draw a little dashed line for the last one, AI and Rydberg state, to distinguish it from IP
            if it == len(lambda_steps) - 1:
                self.axes.hlines(tstp, xmin=xval-0.5, xmax=xval+0.5, linestyle='solid', color="k")

            # alignment of labels
            if xval <= 5.:
                halignlam = 'left'
                xloc_lambda = xval + textpad
                halignlev = 'right'
                xloc_levelstr = 10. - textpad
            else:
                halignlam = 'right'
                xloc_lambda = xval - textpad
                halignlev = 'left'
                xloc_levelstr = textpad

            if not forbidden_steps[it] or not self.parent.rbtn_sett_nodisparrow.isChecked():
                # wavelength text
                lambdastr = '%.*f' %(int(prec_lambda), lambda_steps[it]) + '$\,$nm'
                if it == 0 and len(wavenumber_es) > 0:
                    self.axes.text(firstarrowxmfl + textpad, tstp - wstp/2., lambdastr, color=col, ha=halignlam,
                                   va='center', rotation=90, size=fsz_labels)
                else:
                    self.axes.text(xval + textpad, tstp - wstp/2., lambdastr, color=col, ha=halignlam, va='center',
                                   rotation=90, size=fsz_labels)

            # level text
            if term_symb[it] is None:
                levelstr = '%.*f' %(int(prec_level), tstp) + '$\,$cm$^{-1}$'
            else:
                levelstr = '%.*f' %(int(prec_level), tstp) + '$\,$cm$^{-1}$' + lbreak + term_symb[it]
            if it == len(lambda_steps) - 1:
                leveltextypos = tstp
                leveltextvaalign = 'center'
            else:
                leveltextypos = tstp - 0.01 * totwavenumber_photons
                leveltextvaalign = 'top'
            self.axes.text(xloc_levelstr, leveltextypos, levelstr, color='k', ha=halignlev, va=leveltextvaalign,
                           size=fsz_labels)

            # update yval_bott
            yval_bott = transition_steps[it]

        # create ground state lambda step array
        lambda_step_es = []
        for it in range(len(wavenumber_es)):
            lambda_step_es.append(1.e7 / (1.e7/lambda_steps[0] - (float(wavenumber_es[it]) - float(wavenumber_gs))))

        # now go through low lying excited states
        for it in range(len(wavenumber_es)):
            if lambda_step_es[it] >= 700:
                col = self.colir
            elif 500. < lambda_step_es[it] < 700.:
                col = self.colpump
            elif 350. < lambda_step_es[it] <= 500.:
                col = self.coluv
            else:
                col = self.colfuv

            # values
            xval = firstarrowxmfl + 1.5 + it * 1.5
            yval = mfld_yinc*ipvalue*(1+it)
            wstp = float(wavenumber_steps[0]) - yval

            if not forbidden_es[it] or not self.parent.rbtn_sett_nodisparrow.isChecked():
                # xvalue for arrow
                self.axes.arrow(xval, yval, 0, wstp, width=sett_arr, fc=col, ec=col, length_includes_head=True,
                                head_width=sett_arr_head, head_length=totwavenumber_photons / 30.)

                # print cross out if necessary
                if forbidden_es[it]:
                    yval_cross = yval + wstp / 2.
                    self.axes.plot(xval, yval_cross, 'x', color='r', markersize=20,
                                   markeredgewidth=5.)

                # wavelength text
                lambdastr = '%.*f' %(int(prec_lambda), lambda_step_es[it]) + '$\,$nm'
                self.axes.text(xval + textpad, yval + wstp/2., lambdastr, color=col, ha='left', va='center', rotation=90,
                               size=fsz_labels)

            # level text
            if term_symb_es_formatted[it] is None:
                levelstr = '%.*f' %(int(prec_level), float(wavenumber_es[it])) + '$\,$cm$^{-1}$'
            else:
                # NO LINEBREAK HERE ON THESE LINES!
                levelstr = '%.*f' %(int(prec_level),float(wavenumber_es[it])) + '$\,$cm$^{-1}$, ' + \
                           term_symb_es_formatted[it]
            self.axes.text(xval + 0.5, yval, levelstr, color='k', ha='left', va='bottom', size=fsz_labels)

        # Title:
        title_entry = self.parent.edt_sett_plttitle.text()
        if title_entry is not '':
            self.axes.set_title(title_entry, size=fsz_title)

        # ylabel
        if self.parent.chk_sett_showcmax.isChecked():
            self.axes.set_ylabel('Wavenumber (cm$^{-1}$)', size=fsz_axes_labels)
        else:
            self.axes.axes.get_yaxis().set_ticks([])

        # axis limits
        self.axes.set_xlim([0., 10.])
        self.axes.set_ylim([0., ymax])

        # eV axis on the right
        if self.parent.chk_sett_showevax.isChecked():
            a2.set_ylabel('Energy (eV)', size=fsz_axes_labels)
        else:
            a2.axes.get_yaxis().set_ticks([])
        a2.set_ylim([0., ymax / 8065.54429])

        # remove x ticks
        self.axes.axes.get_xaxis().set_ticks([])

        # tight layout of figure
        self.figure.tight_layout()

        if self.saveplt:
            # get save filename
            # dialog to query filename
            # home folder of user platform independent
            print(self.figure.get_dpi())
            home = expanduser('~')
            # options
            options = QFileDialog.Options()
            # create filetypes
            filetypes = [['PDF Files (*.pdf)', '.pdf'], ['SVG Files (*.svg)', '.svg'], ['PNG Files (*.png)', '.png'],
                         ['EPS File (*.eps)', '.eps'], ['All Files (*.*)', '.pdf']]
            ftypeopt = ''
            for it in filetypes:
                ftypeopt += it[0] + ';;'
            # remove last ;;
            ftypeopt = ftypeopt[0:-2]
            # options |= QFileDialog.DontUseNativeDialog
            filename, filetp = QFileDialog.getSaveFileName(self, 'QFileDialog.getOpenFileName()', home,
                                                           filter=ftypeopt, options=options)
            if filename is not '':
                if filename.find('.') == -1:
                    for it in filetypes:
                        if filetp == it[0]:
                            filename += it[1]
                # save the file
                self.figure.savefig(filename)


def term_to_string(tstr):
    """
    Converts a term symbol string to a LaTeX enabled matplotlib string
    :param tstr:   string to convert
    :return:       string LaTeX enabled for Matplotlib
    """
    if tstr == '':
        return None

    # some exceptionslike AI and IP
    if tstr == 'IP':
        return 'IP'
    if tstr == 'AI':
        return 'AI'
    if tstr == 'Rydberg':
        return 'Rydberg'
    if tstr == 'Ryd':
        return 'Ryd'

    # if there is an equal sign in there, leave it as is
    if tstr.find('=') != -1:
        return tstr

    # find the first slash and start looking for the letter after that
    start = tstr.find('/') + 1
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
    tmp1 = '$^{' + tstr[0:letterind] + '}$'
    tmp2 = tstr[letterind]
    tmp3 = '$_{' + tstr[letterind+1:] + '}$'

    return tmp1+tmp2+tmp3
