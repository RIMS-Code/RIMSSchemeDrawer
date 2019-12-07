from fbs_runtime.application_context.PyQt5 import ApplicationContext

from PyQt5.QtWidgets import QWidget, QMainWindow, QAction, QPushButton, QRadioButton, QCheckBox, QButtonGroup, \
    QTabWidget, QMessageBox, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QFileDialog
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.Qt import QSize
from PyQt5.QtGui import QFont, QDoubleValidator, QIntValidator, QIcon

import functools
import numpy as np
import sys

# plotter - the heart of the whole thing
class Plotter(QWidget):
    def __init__(self, parent, fname=None):
        self.parent = parent

        # now plot the scheme
        self.plotit()

    def plotit(self, fname=None):
        # textpad
        textpad = 0.4
        # percentage to increase for manifold
        mfld_yinc = 0.04   # in # of ipvalue
        #
        firstarrowxmfl = 1.

        # gett settings from program
        # font sizes
        fsz_title = int(self.parent.edt_sett_fstitle.text())
        fsz_axes = int(self.parent.edt_sett_fsaxes.text())
        fsz_axes_labels = int(self.parent.edt_sett_fsaxlbl.text())
        fsz_labels = int(self.parent.edt_sett_fslbl.text())
        sett_headspace = float(self.parent.edt_sett_headspace.text())
        sett_arr = float(self.parent.edt_sett_arrwidth.text())
        sett_arr_head = float(self.parent.edt_sett_arrheadwidth.text())
        prec_lambda = int(self.parent.edt_sett_preclambda.text())
        prec_level = int(self.parent.edt_sett_preclevel.text())

        # throw an error if not at least one box is filled
        if self.parent.edt_level[0].text() == '':
            QMessageBox.warning(self, 'No entries', 'Need at least one level to make a plot!', QMessageBox.Ok)
            return

        # let's first get the wavelengths that we want
        lambdas = []
        for it in range(self.parent.numberofsteps):
            lambdas.append(self.parent.edt_level[it].text())

        # now only add lambdas that are NOT low lying states!
        lambda_steps = []
        for it in range(self.parent.numberofsteps):
            if not self.parent.chk_lowlying[it].isChecked():
                lambda_steps.append(lambdas[it])

        try:
            ipvalue = float(self.parent.edt_iplevel.text())
        except ValueError:
            QMessageBox.warning(self, 'Enter IP', 'Please enter an ionization potential as a number and try again.',
                                QMessageBox.Ok)
            return

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

        # get more ground states if available
        wavenumber_es = []
        term_symb_es = []
        for it in range(self.parent.numberofsteps):
            if self.parent.chk_lowlying[it].isChecked():
                wavenumber_es.append(float(self.parent.edt_level[it].text()))
                term_symb_es.append(self.parent.edt_term[it].text())

        # create wavenumber array
        wavenumber_steps = 1. / lambda_steps * 1e7

        transition_steps = np.zeros(len(wavenumber_steps))
        transition_steps[0] = wavenumber_steps[0] + wavenumber_gs
        for it in range(1, len(transition_steps)):
            transition_steps[it] = transition_steps[it-1] + wavenumber_steps[it]

        # calculate total excitation in wavenumbers - for scaling later
        totwavenumber_photons = np.sum(wavenumber_steps)

        # ymax:   # fixme to check: is this really wavenumber_gs here? need to see if it looks right in the plot
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


        # # file name given or show what you can do?
        # if fname is None:
        #     # create the new window
        #     pltwin = tk.Toplevel()
        #
        # # break line or put in comma, depending on option
        # lbreak = ', '
        # if self.chk_sett_linebreaks.isChecked():
        #     lbreak = '\n'
        #
        # # ### CREATE FIGURE ###
        # # tick size
        # matplotlib.rc('xtick', labelsize=fsz_axes)
        # matplotlib.rc('ytick', labelsize=fsz_axes)
        #
        # f = Figure(figsize=(float(self.wh_width.get()), float(self.wh_height.get())), dpi=100)
        # a = f.add_subplot(111)
        # # second axis for eV
        # a2 = a.twinx()
        #
        # # tick label in scientific notation
        # # a.ticklabel_format(style='sci', scilimits=(-3, 3), axis='both')
        # fform = matplotlib.ticker.ScalarFormatter(useOffset=False, useMathText=True)
        # gform = lambda x, pos: "${}$".format(fform._formatSciNotation('%1.10e' % x))
        # a.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(gform))
        # a2.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(gform))
        #
        # # shade the level above the IP
        # xshade = [0., 10.]
        # a.fill_between(xshade, ipvalue, ymax, facecolor='#adbbff', alpha=0.5)
        # # label the IP
        # if self.sett_ip_label_pos_variable.get() == 0:
        #     iplabelypos = ipvalue + 0.01*totwavenumber_photons
        #     iplabelyalign = 'bottom'
        # else:
        #     iplabelypos = ipvalue - 0.01 * totwavenumber_photons
        #     iplabelyalign = 'top'
        # if term_symb_ip is None:
        #     iplabelstr = 'IP, %.*f' %(int(prec_level), ipvalue) + '$\,$cm$^{-1}$'
        # else:
        #     iplabelstr = 'IP, %.*f' %(int(prec_level), ipvalue) + '$\,$cm$^{-1}$' + lbreak + term_symb_ip
        # # ip above or below
        # a.text(textpad, iplabelypos, iplabelstr, color='k', ha='left', va=iplabelyalign, size=fsz_labels)
        #
        # # Draw the vertical lines for every transition and IP, unless transition is above IP (shade area there)
        # for it in transition_steps:
        #     if it < ipvalue:
        #         a.hlines(it, xmin=0, xmax=10)
        # # Lines for manifold groundstater
        # for it in range(len(wavenumber_es)):
        #     a.hlines(mfld_yinc*ipvalue*(1+it), xmin=1.5*it+2.3, xmax=1.5*it+3.7,
        #              linestyle='solid')
        #
        # # Draw the vertical lines for every transition and IP, unless transition is above IP (shade area there)
        # for it in transition_steps:
        #     if it < ipvalue:
        #         a.hlines(it, xmin=0, xmax=10)
        #
        # # draw the state we come out of, if not ground state
        # if float(self.ground_state_value.get()) > 0.:
        #     a.hlines(float(self.ground_state_value.get()), xmin=0, xmax=10)
        #
        # # draw the arrows
        # deltax = 8.65 / (len(lambda_steps) + 1.) - 0.5
        # xval = 0.
        # yval_bott = float(self.ground_state_value.get())
        # # put in bottom level
        # if term_symb_gs is None:
        #     levelstr = '%.*f' %(int(prec_level), wavenumber_gs) + '$\,$cm$^{-1}$'
        # else:
        #     levelstr = '%.*f' %(int(prec_level), wavenumber_gs) + '$\,$cm$^{-1}$' + lbreak + term_symb_gs
        # a.text(10. - textpad, float(self.ground_state_value.get()), levelstr, color='k', ha='right', va='bottom',
        #        size=fsz_labels)
        #
        # for it in range(len(lambda_steps)):
        #     if lambda_steps[it] >= 700:
        #         col = self.colir
        #     elif 500. < lambda_steps[it] < 700.:
        #         col = self.colpump
        #     elif 350. < lambda_steps[it] <= 500.:
        #         col = self.coluv
        #     else:
        #         col = self.colfuv
        #     # xvalue for arrow
        #     xval += deltax
        #     wstp = wavenumber_steps[it]
        #     tstp = transition_steps[it]
        #     if it == 0 and len(wavenumber_es) > 0:
        #         a.arrow(firstarrowxmfl, yval_bott, 0, wstp, width=sett_arr, fc=col, ec=col, length_includes_head=True,
        #                 head_width=sett_arr_head, head_length=totwavenumber_photons/30.)
        #     else:
        #         a.arrow(xval, yval_bott, 0, wstp, width=sett_arr, fc=col, ec=col, length_includes_head=True,
        #                 head_width=sett_arr_head, head_length=totwavenumber_photons / 30.)
        #
        #     # draw a little dashed line for the last one, AI and Rydberg state, to distinguish it from IP
        #     if it == len(lambda_steps) - 1:
        #         a.hlines(tstp, xmin=xval-0.5, xmax=xval+0.5, linestyle='solid')
        #
        #     # alignment of labels
        #     if xval <= 5.:
        #         halignlam = 'left'
        #         xloc_lambda = xval + textpad
        #         halignlev = 'right'
        #         xloc_levelstr = 10. - textpad
        #     else:
        #         halignlam = 'right'
        #         xloc_lambda = xval - textpad
        #         halignlev = 'left'
        #         xloc_levelstr = textpad
        #
        #     # wavelength text
        #     lambdastr = '%.*f' %(int(prec_lambda), lambda_steps[it]) + '$\,$nm'
        #     if it == 0 and len(wavenumber_es) > 0:
        #         a.text(firstarrowxmfl + textpad, tstp - wstp/2., lambdastr, color=col, ha=halignlam, va='center',
        #                rotation=90, size=fsz_labels)
        #     else:
        #         a.text(xval + textpad, tstp - wstp/2., lambdastr, color=col, ha=halignlam, va='center', rotation=90,
        #                size=fsz_labels)
        #
        #     print(lambda_steps[it])
        #     # level text
        #     if term_symb[it] is None:
        #         levelstr = '%.*f' %(int(prec_level), tstp) + '$\,$cm$^{-1}$'
        #     else:
        #         levelstr = '%.*f' %(int(prec_level), tstp) + '$\,$cm$^{-1}$' + lbreak + term_symb[it]
        #     if it == len(lambda_steps) - 1:
        #         leveltextypos = tstp
        #         leveltextvaalign = 'center'
        #     else:
        #         leveltextypos = tstp - 0.01 * totwavenumber_photons
        #         leveltextvaalign = 'top'
        #     a.text(xloc_levelstr, leveltextypos, levelstr, color='k', ha=halignlev, va=leveltextvaalign,
        #            size=fsz_labels)
        #
        #     # update yval_bott
        #     yval_bott = transition_steps[it]
        #
        # # create ground state lambda step array
        # lambda_step_es = []
        # for it in range(len(wavenumber_es)):
        #     lambda_step_es.append(1.e7 / (1.e7/lambda_steps[0] - (float(wavenumber_es[it]) - float(wavenumber_gs))))
        #
        # # now go through low lying excited states
        # for it in range(len(wavenumber_es)):
        #     if lambda_step_es[it] >= 700:
        #         col = self.colir
        #     elif 500. < lambda_step_es[it] < 700.:
        #         col = self.colpump
        #     elif 350. < lambda_step_es[it] <= 500.:
        #         col = self.coluv
        #     else:
        #         col = self.colfuv
        #     # xvalue for arrow
        #     xval = firstarrowxmfl + 1.5 + it * 1.5
        #     yval = mfld_yinc*ipvalue*(1+it)
        #     wstp = float(wavenumber_steps[0]) - yval
        #     a.arrow(xval, yval, 0, wstp, width=sett_arr, fc=col, ec=col, length_includes_head=True,
        #             head_width=sett_arr_head, head_length=totwavenumber_photons / 30.)
        #
        #     # wavelength text
        #     lambdastr = '%.*f' %(int(prec_lambda), lambda_step_es[it]) + '$\,$nm'
        #     a.text(xval + textpad, yval + wstp/2., lambdastr, color=col, ha='left', va='center', rotation=90,
        #            size=fsz_labels)
        #
        #     # level text
        #     if term_symb_es_formatted[it] is None:
        #         levelstr = '%.*f' %(int(prec_level), float(wavenumber_es[it])) + '$\,$cm$^{-1}$'
        #     else:
        #         # NO LINEBREAK HERE ON THESE LINES!
        #         levelstr = '%.*f' %(int(prec_level),float(wavenumber_es[it])) + '$\,$cm$^{-1}$, ' + \
        #                    term_symb_es_formatted[it]
        #     a.text(xval + 0.5, yval, levelstr, color='k', ha='left', va='bottom', size=fsz_labels)
        #
        # # Title:
        # if self.title_entry is not '':
        #     a.set_title(self.title_entry.get(), size=fsz_title)
        #
        # # ylabel
        # a.set_ylabel('Wavenumber (cm$^{-1}$)', size=fsz_axes_labels)
        # # axis limits
        # a.set_xlim([0., 10.])
        # a.set_ylim([0., ymax])
        #
        # # eV axis on the right
        # a2.set_ylabel('Energy (eV)', size=fsz_axes_labels)
        # a2.set_ylim([0., ymax / 8065.54429])
        #
        # # remove x ticks
        # a.axes.get_xaxis().set_ticks([])
        #
        # # tight layout of figure
        # f.tight_layout()

        # if fname is None:
        #     # a tk.DrawingArea
        #     canvas = FigureCanvasTkAgg(f, master=pltwin)
        #     canvas.show()
        #     canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #
        #     toolbar = NavigationToolbar2TkAgg(canvas, pltwin)
        #     toolbar.update()
        #     canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # else:
        #     f.savefig(fname)



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
