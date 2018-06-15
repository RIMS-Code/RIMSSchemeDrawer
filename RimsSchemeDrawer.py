# Import Tkinter
try:
    import Tkinter as tk
    import tkFont as tkFont
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox
    import tkSimpleDialog as simpledialog
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import tkFont
    from tkinter import filedialog
    from tkinter import messagebox
    from tkinter import simpledialog
    import tkinter.ttk as ttk
import numpy as np
import platform

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings


from matplotlib.figure import Figure


class RSD:
    def __init__(self, master):
        # Colors for arrows
        self.colir = '#a00000'
        self.coluv = '#0012a0'
        self.colfuv = '#5f00a0'
        self.colpump = '#0aa000'

        # Program and stuff
        self.master = master
        master.title("RIMS Scheme Drawer")

        # Geometry and stuff
        rows, cols = 11, 7
        BW, BH, pad = 120, 30, 15
        winsize = ((1.5 + cols / 2) * pad + cols * BW,
                   (1.5 + rows / 2) * pad + rows * BH,
                   10, 10)  # width, height, xoffset, yoffset
        self.rows, self.cols = rows, cols
        self.BW, self.BH, self.pad = BW, BH, pad
        self.winsize = winsize

        # set master size
        master.geometry("%dx%d+%d+%d" % winsize)

        # font formatting OS dependent
        if platform.system() == 'Darwin':
            fontsize = 11
            self.fontsize = fontsize
        else:
            fontsize = 9
            self.fontsize = fontsize

        # font formatting
        self.font_std = tkFont.Font(size=fontsize)
        self.font_bold = tkFont.Font(size=fontsize, weight=tkFont.BOLD)
        self.font_ital = tkFont.Font(size=fontsize, slant=tkFont.ITALIC)

        # radiobutton for nm or cm-1
        self.unitvar = tk.IntVar()
        self.unit_selector_nm = tk.Radiobutton(master, text='nm', anchor=tk.W, font=self.font_std,
                                               variable=self.unitvar, value=1, command=self.setsteplabels)
        self.unit_selector_nm.place(x=self.x(1), y=self.y(1), width=BW/2, height=BH)
        self.unit_selector_cm = tk.Radiobutton(master, text='cm^-1', anchor=tk.E, font=self.font_std,
                                               variable=self.unitvar, value=2, command=self.setsteplabels)
        self.unit_selector_cm.place(x=self.x(1.5), y=self.y(1), width=BW/2, height=BH)
        self.unit_selector_cm.select()

        # box for Ground state
        self.ground_state_label = tk.Label(master, text='Ground state (cm^-1)', anchor=tk.W, font=self.font_std)
        self.ground_state_label.place(x=self.x(1), y=self.y(2), width=BW, height=BH)
        self.ground_state_value = tk.Entry(master)
        self.ground_state_value.place(x=self.x(2), y=self.y(2), width=BW, height=BH)

        # Wavenlength entry boxes
        self.step1_lambda = tk.Entry(master)
        self.step2_lambda = tk.Entry(master)
        self.step3_lambda = tk.Entry(master)
        self.step4_lambda = tk.Entry(master)
        self.step5_lambda = tk.Entry(master)
        self.step1_lambda.place(x=self.x(2), y=self.y(3), width=BW, height=BH)
        self.step2_lambda.place(x=self.x(2), y=self.y(4), width=BW, height=BH)
        self.step3_lambda.place(x=self.x(2), y=self.y(5), width=BW, height=BH)
        self.step4_lambda.place(x=self.x(2), y=self.y(6), width=BW, height=BH)
        self.step5_lambda.place(x=self.x(2), y=self.y(7), width=BW, height=BH)

        # label and box for IP
        self.ip_label = tk.Label(master, text='IP (cm^-1):', anchor=tk.W, font=self.font_std)
        self.ip_label.place(x=self.x(1), y=self.y(8), width=BW, height=BH)
        self.ip_value = tk.Entry(master)
        self.ip_value.place(x=self.x(2), y=self.y(8), width=BW, height=BH)

        # Term symbols title and entry
        self.termgs = tk.Entry(master)
        self.term_label = tk.Label(master, text='Term Symbol', anchor=tk.W, font=self.font_bold)
        self.term_label.place(x=self.x(3), y=self.y(1), width=BW, height=BH)
        self.term1 = tk.Entry(master)
        self.term2 = tk.Entry(master)
        self.term3 = tk.Entry(master)
        self.term4 = tk.Entry(master)
        self.term5 = tk.Entry(master)
        self.termip = tk.Entry(master)
        self.termgs.place(x=self.x(3), y=self.y(2), width=BW, height=BH)
        self.term1.place(x=self.x(3), y=self.y(3), width=BW, height=BH)
        self.term2.place(x=self.x(3), y=self.y(4), width=BW, height=BH)
        self.term3.place(x=self.x(3), y=self.y(5), width=BW, height=BH)
        self.term4.place(x=self.x(3), y=self.y(6), width=BW, height=BH)
        self.term5.place(x=self.x(3), y=self.y(7), width=BW, height=BH)
        self.termip.place(x=self.x(3), y=self.y(8), width=BW, height=BH)

        # Part of GS manifold
        self.mf_label = tk.Label(master, text='GS Manifold?', anchor=tk.W, font=self.font_bold)
        self.mf_label.place(x=self.x(4), y=self.y(1), width=BW, height=BH)
        self.mf1_var = tk.IntVar()
        self.mf1_box = tk.Checkbutton(master, text='Low-lying state?', justify=tk.LEFT,
                                      variable=self.mf1_var, font=self.font_std, command=self.setsteplabels)
        self.mf1_box.place(x=self.x(4), y=self.y(3), width=BW, height=BH)
        self.mf2_var = tk.IntVar()
        self.mf2_box = tk.Checkbutton(master, text='Low-lying state?', justify=tk.LEFT,
                                      variable=self.mf2_var, font=self.font_std, command=self.setsteplabels)
        self.mf2_box.place(x=self.x(4), y=self.y(4), width=BW, height=BH)
        self.mf3_var = tk.IntVar()
        self.mf3_box = tk.Checkbutton(master, text='Low-lying state?', justify=tk.LEFT,
                                      variable=self.mf3_var, font=self.font_std, command=self.setsteplabels)
        self.mf3_box.place(x=self.x(4), y=self.y(5), width=BW, height=BH)
        self.mf4_var = tk.IntVar()
        self.mf4_box = tk.Checkbutton(master, text='Low-lying state?', justify=tk.LEFT,
                                      variable=self.mf4_var, font=self.font_std, command=self.setsteplabels)
        self.mf4_box.place(x=self.x(4), y=self.y(6), width=BW, height=BH)

        # ### SETTINGS ###
        # width, height to set
        self.sett_label = tk.Label(master, text='Settings', anchor=tk.W, font=self.font_bold)
        self.sett_label.place(x=self.x(5), y=self.y(1), width=2*BW, height=BH)
        self.wh_label = tk.Label(master, text='Figure Width x Height:', anchor=tk.W, font=self.font_std)
        self.wh_label.place(x=self.x(5), y=self.y(2), width=BW, height=BH)
        self.wh_width = tk.Entry(master)
        self.wh_height = tk.Entry(master)
        self.wh_times = tk.Label(master, text='x', anchor=tk.W, font=self.font_std)
        self.wh_width.place(x=self.x(6), y=self.y(2), width=0.45 * BW, height=BH)
        self.wh_times.place(x=self.x(6.45), y=self.y(2), width=0.1 * BW, height=BH)
        self.wh_height.place(x=self.x(6.55), y=self.y(2), width=0.45 * BW, height=BH)
        self.fsz_title_label = tk.Label(master, text='Font size title:', anchor=tk.W, font=self.font_std)
        self.fsz_ax_num_label = tk.Label(master, text='Font size axes:', anchor=tk.W, font=self.font_std)
        self.fsz_ax_lbl_label = tk.Label(master, text='Font size axes label:', anchor=tk.W, font=self.font_std)
        self.fsz_lbls_label = tk.Label(master, text='Font size labels:', anchor=tk.W, font=self.font_std)
        self.sett_headspace = tk.Label(master, text='Headspace (cm^-1):', anchor=tk.W, font=self.font_std)
        self.sett_arr_lbl = tk.Label(master, text='Arrow width:', anchor=tk.W, font=self.font_std)
        self.sett_arr_head_lbl = tk.Label(master, text='Arrow head width:', anchor=tk.W, font=self.font_std)
        self.sett_prec_lambda_label = tk.Label(master, text='Precision wavlength:', anchor=tk.W, font=self.font_std)
        self.sett_prec_level_label = tk.Label(master, text='Precision level:', anchor=tk.W, font=self.font_std)
        self.fsz_title_label.place(x=self.x(5), y=self.y(3), width=BW, height=BH)
        self.fsz_ax_num_label.place(x=self.x(5), y=self.y(4), width=BW, height=BH)
        self.fsz_ax_lbl_label.place(x=self.x(5), y=self.y(5), width=BW, height=BH)
        self.fsz_lbls_label.place(x=self.x(5), y=self.y(6), width=BW, height=BH)
        self.sett_headspace.place(x=self.x(5), y=self.y(7), width=BW, height=BH)
        self.sett_arr_lbl.place(x=self.x(5), y=self.y(8), width=BW, height=BH)
        self.sett_arr_head_lbl.place(x=self.x(5), y=self.y(9), width=BW, height=BH)
        self.sett_prec_lambda_label.place(x=self.x(5), y=self.y(10), width=BW, height=BH)
        self.sett_prec_level_label.place(x=self.x(5), y=self.y(11), width=BW, height=BH)
        self.fsz_title_entry = tk.Entry(master)
        self.fsz_ax_num_entry = tk.Entry(master)
        self.fsz_ax_lbl_entry = tk.Entry(master)
        self.fsz_lbls_entry = tk.Entry(master)
        self.sett_headspace_entry = tk.Entry(master)
        self.sett_arr_entry = tk.Entry(master)
        self.sett_arr_head_entry = tk.Entry(master)
        self.sett_prec_lambda_entry = tk.Entry(master)
        self.sett_prec_level_entry = tk.Entry(master)
        self.fsz_title_entry.place(x=self.x(6), y=self.y(3), width=BW, height=BH)
        self.fsz_ax_num_entry.place(x=self.x(6), y=self.y(4), width=BW, height=BH)
        self.fsz_ax_lbl_entry.place(x=self.x(6), y=self.y(5), width=BW, height=BH)
        self.fsz_lbls_entry.place(x=self.x(6), y=self.y(6), width=BW, height=BH)
        self.sett_headspace_entry.place(x=self.x(6), y=self.y(7), width=BW, height=BH)
        self.sett_arr_entry.place(x=self.x(6), y=self.y(8), width=BW, height=BH)
        self.sett_arr_head_entry.place(x=self.x(6), y=self.y(9), width=BW, height=BH)
        self.sett_prec_lambda_entry.place(x=self.x(6), y=self.y(10), width=BW, height=BH)
        self.sett_prec_level_entry.place(x=self.x(6), y=self.y(11), width=BW, height=BH)
        # Title
        self.title_label = tk.Label(master, text='Plot Title', anchor=tk.W, font=self.font_bold)
        self.title_label.place(x=self.x(7), y=self.y(1), width=BW, height=BH)
        self.title_entry = tk.Entry(master)
        self.title_entry.place(x=self.x(7), y=self.y(2), width=BW, height=BH)

        # Buttons
        self.button_plot = tk.Button(master, text='Plot', font=self.font_std, command=self.plotter)
        self.button_save = tk.Button(master, text='Save', font=self.font_std, command=self.save)
        # test button
        # self.button_test = tk.Button(master, text='Test', font=self.font_std, command=self.test)
        self.button_help = tk.Button(master, text='Help', font=self.font_std, command=self.help)
        self.button_quit = tk.Button(master, text='Quit', font=self.font_std, command=self.quit)
        self.button_plot.place(x=self.x(7), y=self.y(3), width=BW, height=BH)
        self.button_save.place(x=self.x(7), y=self.y(4), width=BW, height=BH)
        # self.button_test.place(x=self.x(5), y=self.y(6), width=BW, height=BH)
        self.button_help.place(x=self.x(7), y=self.y(8), width=BW, height=BH)
        self.button_quit.place(x=self.x(7), y=self.y(9), width=BW, height=BH)

        # Options
        self.opt_linebreak_st = tk.IntVar()
        self.opt_linebreak = tk.Checkbutton(master, text='Linebreaks?', justify=tk.LEFT,
                                            variable=self.opt_linebreak_st, font=self.font_std)
        self.opt_linebreak.place(x=self.x(7), y=self.y(5), width=BW, height=BH)

        # set step labels
        self.setsteplabels()

        # set settings
        self.wh_width.insert(tk.END, '5')
        self.wh_height.insert(tk.END, '8')
        self.fsz_title_entry.insert(tk.END, '14')
        self.fsz_ax_num_entry.insert(tk.END, '10')
        self.fsz_ax_lbl_entry.insert(tk.END, '14')
        self.fsz_lbls_entry.insert(tk.END, '12')
        self.sett_headspace_entry.insert(tk.END, '2000')
        self.sett_arr_entry.insert(tk.END, '0.2')
        self.sett_arr_head_entry.insert(tk.END, '0.6')
        self.sett_prec_lambda_entry.insert(tk.END, '3')
        self.sett_prec_level_entry.insert(tk.END, '0')

        # fixme: temporary insert, remove later
        # self.ground_state_value.insert(tk.END, '0.')
        # self.step1_lambda.insert(tk.END, '200.')
        # self.mf1_box.select()
        # self.step2_lambda.insert(tk.END, '19387')
        # self.step3_lambda.insert(tk.END, '37020')
        # self.ip_value.insert(tk.END, '36000.')

    def setsteplabels(self):
        # set unit
        if self.unitvar.get() == 1:
            unit = 'nm'
        else:
            unit = 'cm^-1'
        # Labels for the given steps (nm)
        self.step_title_label = tk.Label(self.master, text='Level', anchor=tk.W, font=self.font_bold)
        self.step_title_label.place(x=self.x(2), y=self.y(1), width=self.BW, height=self.BH)
        if self.mf1_var.get():
            self.step1_label = tk.Label(self.master, text='Low-lying st (cm^-1):', anchor=tk.W, font=self.font_std)
        else:
            self.step1_label = tk.Label(self.master, text='1st step (' + unit + '):', anchor=tk.W, font=self.font_std)
        if self.mf2_var.get():
            self.step2_label = tk.Label(self.master, text='Low-lying st (cm^-1):', anchor=tk.W, font=self.font_std)
        else:
            self.step2_label = tk.Label(self.master, text='2nd step (' + unit + '):', anchor=tk.W, font=self.font_std)
        if self.mf3_var.get():
            self.step3_label = tk.Label(self.master, text='Low-lying st (cm^-1):', anchor=tk.W, font=self.font_std)
        else:
            self.step3_label = tk.Label(self.master, text='3rd step (' + unit + '):', anchor=tk.W, font=self.font_std)
        if self.mf4_var.get():
            self.step4_label = tk.Label(self.master, text='Low-lying st (cm^-1):', anchor=tk.W, font=self.font_std)
        else:
            self.step4_label = tk.Label(self.master, text='4th step (' + unit + '):', anchor=tk.W, font=self.font_std)
        # label 5
        self.step5_label = tk.Label(self.master, text='5th step (' + unit + '):', anchor=tk.W, font=self.font_std)
        self.step1_label.place(x=self.x(1), y=self.y(3), width=self.BW, height=self.BH)
        self.step2_label.place(x=self.x(1), y=self.y(4), width=self.BW, height=self.BH)
        self.step3_label.place(x=self.x(1), y=self.y(5), width=self.BW, height=self.BH)
        self.step4_label.place(x=self.x(1), y=self.y(6), width=self.BW, height=self.BH)
        self.step5_label.place(x=self.x(1), y=self.y(7), width=self.BW, height=self.BH)

    def x(self, col):
        # Calculates x coordinate of gui element
        return self.pad + 0.5 * (col - 1) * self.pad + (col - 1) * self.BW

    def y(self, row):
        # Calculates y coordinate of gui element
        return self.pad + 0.5 * (row - 1) * self.pad + (row - 1) * self.BH

    def save(self):
        options = dict()
        options['defaultextension'] = '.pdf'
        options['filetypes'] = [('PDF', '.pdf'), ('PNG', '.png'), ('JPG', '.jpg'), ('EPS', '.eps')]
        fname = filedialog.asksaveasfilename(**options)
        self.plotter(fname=fname)

    def plotter(self, fname=None):
        # textpad
        textpad = 0.4
        # percentage to increase for manifold
        mfld_yinc = 0.04   # in # of ipvalue
        #
        firstarrowxmfl = 1.

        # gett settings from program
        # font sizes
        fsz_title = int(self.fsz_title_entry.get())
        fsz_axes = int(self.fsz_ax_num_entry.get())
        fsz_axes_labels = int(self.fsz_ax_lbl_entry.get())
        fsz_labels = int(self.fsz_lbls_entry.get())
        sett_headspace = float(self.sett_headspace_entry.get())
        sett_arr = float(self.sett_arr_entry.get())
        sett_arr_head = float(self.sett_arr_head_entry.get())
        prec_lambda = float(self.sett_prec_lambda_entry.get())
        prec_level = float(self.sett_prec_level_entry.get())

        # let's first get the wavelengths that we want
        lambda1 = self.step1_lambda.get()
        lambda2 = self.step2_lambda.get()
        lambda3 = self.step3_lambda.get()
        lambda4 = self.step4_lambda.get()
        lambda5 = self.step5_lambda.get()

        # now only add lambdas that are NOT low lying states!
        lambda_steps = []
        if not self.mf1_var.get():
            lambda_steps.append(lambda1)
        if not self.mf2_var.get():
            lambda_steps.append(lambda2)
        if not self.mf3_var.get():
            lambda_steps.append(lambda3)
        if not self.mf4_var.get():
            lambda_steps.append(lambda4)
        lambda_steps.append(lambda5)

        try:
            ipvalue = float(self.ip_value.get())
        except ValueError:
            messagebox.showerror('Enter IP', 'Please enter an ionization potential as a number and try again.')
            return

        # get the term symbols that were entered
        term_symb_entered = []
        if not self.mf1_var.get():
            term_symb_entered.append(self.term1.get())
        if not self.mf2_var.get():
            term_symb_entered.append(self.term2.get())
        if not self.mf3_var.get():
            term_symb_entered.append(self.term3.get())
        if not self.mf4_var.get():
            term_symb_entered.append(self.term4.get())
        term_symb_entered.append(self.term5.get())

        # get ground state wavenumber
        if self.ground_state_value.get() is '':
            wavenumber_gs = 0
        else:
            wavenumber_gs = float(self.ground_state_value.get())

        # now go through the lambda steps and transform into actual wavelengths if not already
        if self.unitvar.get() == 2:
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
        if self.mf1_var.get():
            wavenumber_es.append(self.step1_lambda.get())
            term_symb_es.append(self.term1.get())
        if self.mf2_var.get():
            wavenumber_es.append(self.step2_lambda.get())
            term_symb_es.append(self.term2.get())
        if self.mf3_var.get():
            wavenumber_es.append(self.step3_lambda.get())
            term_symb_es.append(self.term3.get())
        if self.mf4_var.get():
            wavenumber_es.append(self.step4_lambda.get())
            term_symb_es.append(self.term4.get())

        # create wavenumber array
        wavenumber_steps = 1. / lambda_steps * 1e7

        transition_steps = np.zeros(len(wavenumber_steps))
        transition_steps[0] = wavenumber_steps[0] + wavenumber_gs
        for it in range(1, len(transition_steps)):
            transition_steps[it] = transition_steps[it-1] + wavenumber_steps[it]

        # calculate total excitation in wavenumbers - for scaling later
        totwavenumber_photons = np.sum(wavenumber_steps)

        # ymax:
        if ipvalue > totwavenumber_photons + float(self.ground_state_value.get()):
            ymax = ipvalue + sett_headspace
        elif totwavenumber_photons + float(self.ground_state_value.get()) - ipvalue < sett_headspace:
            ymax = ipvalue + sett_headspace
        else:
            ymax = totwavenumber_photons + float(self.ground_state_value.get())

        # create term symbol string for direct usage in plotting
        term_symb = []
        term_symb_es_formatted = []
        for it in range(len(wavenumber_steps)):
            term_symb.append(term_to_string(term_symb_entered[it]))
        for it in range(len(term_symb_es)):
            term_symb_es_formatted.append(term_to_string(term_symb_es[it]))
        # get term symbol for ip and gs
        term_symb_ip = term_to_string(self.termip.get())
        term_symb_gs = term_to_string(self.termgs.get())

        # file name given or show what you can do?
        if fname is None:
            # create the new window
            pltwin = tk.Toplevel()

        # break line or put in comma, depending on option
        lbreak = ', '
        if self.opt_linebreak_st.get():
            lbreak = '\n'

        # ### CREATE FIGURE ###
        # tick size
        matplotlib.rc('xtick', labelsize=fsz_axes)
        matplotlib.rc('ytick', labelsize=fsz_axes)

        f = Figure(figsize=(float(self.wh_width.get()), float(self.wh_height.get())), dpi=100)
        a = f.add_subplot(111)
        # second axis for eV
        a2 = a.twinx()

        # shade the level above the IP
        xshade = [0., 10.]
        a.fill_between(xshade, ipvalue, ymax, facecolor='#adbbff', alpha=0.5)
        # label the IP
        if term_symb_ip is None:
            iplabelstr = 'IP, %.*f' %(int(prec_level), ipvalue) + '$\,$cm$^{-1}$'
        else:
            iplabelstr = 'IP, %.*f' %(int(prec_level), ipvalue) + '$\,$cm$^{-1}$' + lbreak + term_symb_ip
        a.text(textpad, ipvalue + 0.01*totwavenumber_photons, iplabelstr, color='k', ha='left', size=fsz_labels)

        # Draw the vertical lines for every transition and IP, unless transition is above IP (shade area there)
        for it in transition_steps:
            if it < ipvalue:
                a.hlines(it, xmin=0, xmax=10)
        # Lines for manifold groundstater
        for it in range(len(wavenumber_es)):
            a.hlines(mfld_yinc*ipvalue*(1+it), xmin=1.5*it+2.3, xmax=1.5*it+3.7,
                     linestyle='dashed')

        # Draw the vertical lines for every transition and IP, unless transition is above IP (shade area there)
        for it in transition_steps:
            if it < ipvalue:
                a.hlines(it, xmin=0, xmax=10)

        # draw the state we come out of, if not ground state
        if float(self.ground_state_value.get()) > 0.:
            a.hlines(float(self.ground_state_value.get()), xmin=0, xmax=10)

        # draw the arrows
        deltax = 8.65 / (len(lambda_steps) + 1.) - 0.5
        xval = 0.
        yval_bott = float(self.ground_state_value.get())
        # put in bottom level
        if term_symb_gs is None:
            levelstr = '%.*f' %(int(prec_level), wavenumber_gs) + '$\,$cm$^{-1}$'
        else:
            levelstr = '%.*f' %(int(prec_level), wavenumber_gs) + '$\,$cm$^{-1}$' + lbreak + term_symb_gs
        a.text(10. - textpad, float(self.ground_state_value.get()), levelstr, color='k', ha='right', va='bottom',
               size=fsz_labels)

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
            if it == 0 and len(wavenumber_es) > 0:
                a.arrow(firstarrowxmfl, yval_bott, 0, wstp, width=sett_arr, fc=col, ec=col, length_includes_head=True,
                        head_width=sett_arr_head, head_length=totwavenumber_photons/30.)
            else:
                a.arrow(xval, yval_bott, 0, wstp, width=sett_arr, fc=col, ec=col, length_includes_head=True,
                        head_width=sett_arr_head, head_length=totwavenumber_photons / 30.)

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

            # wavelength text
            lambdastr = '%.*f' %(int(prec_lambda), lambda_steps[it]) + '$\,$nm'
            if it == 0 and len(wavenumber_es) > 0:
                a.text(firstarrowxmfl + textpad, tstp - wstp/2., lambdastr, color=col, ha=halignlam, va='center',
                       rotation=90, size=fsz_labels)
            else:
                a.text(xval + textpad, tstp - wstp/2., lambdastr, color=col, ha=halignlam, va='center', rotation=90,
                       size=fsz_labels)

            # level text
            if term_symb[it] is None:
                levelstr = '%.*f' %(int(prec_level), tstp) + '$\,$cm$^{-1}$'
            else:
                levelstr = '%.*f' %(int(prec_level), tstp) + '$\,$cm$^{-1}$' + lbreak + term_symb[it]
            a.text(xloc_levelstr, tstp - 0.01*totwavenumber_photons, levelstr, color='k', ha=halignlev, va='top',
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
            # xvalue for arrow
            xval = firstarrowxmfl + 1.5 + it * 1.5
            yval = mfld_yinc*ipvalue*(1+it)
            wstp = float(wavenumber_steps[0]) - yval
            a.arrow(xval, yval, 0, wstp, width=sett_arr, fc=col, ec=col, length_includes_head=True,
                    head_width=sett_arr_head, head_length=totwavenumber_photons / 30.)

            # wavelength text
            lambdastr = '%.*f' %(int(prec_lambda), lambda_step_es[it]) + '$\,$nm'
            a.text(xval + textpad, yval + wstp/2., lambdastr, color=col, ha='left', va='center', rotation=90,
                   size=fsz_labels)

            # level text
            if term_symb_es_formatted[it] is None:
                levelstr = '%.*f' %(int(prec_level), float(wavenumber_es[it])) + '$\,$cm$^{-1}$'
            else:
                # NO LINEBREAK HERE ON THESE LINES!
                levelstr = '%.*f' %(int(prec_level),float(wavenumber_es[it])) + '$\,$cm$^{-1}$, ' + \
                           term_symb_es_formatted[it]
            a.text(xval + 0.5, yval, levelstr, color='k', ha='left', va='bottom', size=fsz_labels)

        # Title:
        if self.title_entry is not '':
            a.set_title(self.title_entry.get(), size=fsz_title)

        # ylabel
        a.set_ylabel('Wavenumber (cm$^{-1}$)', size=fsz_axes_labels)
        # axis limits
        a.set_xlim([0., 10.])
        a.set_ylim([0., ymax])

        # eV axis on the right
        a2.set_ylabel('Energy (eV)', size=fsz_axes_labels)
        a2.set_ylim([0., ymax / 8065.54429])

        # remove x ticks
        a.axes.get_xaxis().set_ticks([])

        # tight layout of figure
        f.tight_layout()

        if fname is None:
            # a tk.DrawingArea
            canvas = FigureCanvasTkAgg(f, master=pltwin)
            canvas.show()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            toolbar = NavigationToolbar2TkAgg(canvas, pltwin)
            toolbar.update()
            canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        else:
            f.savefig(fname)

    def test(self):
        print self.unitvar.get()

    def help(self):
        messagebox.showinfo('Help', 'This program can be used to automatically generate RIMS scheme figures that look '
                                    'pretty. You can either plot them and look at them on screen, or save them in a '
                                    'variety of formats. Available formats are:\n'
                                    '  * .pdf (vector graphic, default)\n'
                                    '  * .eps (vector graphic\n'
                                    '  * .png\n\n'
                                    '  * Term signs have to be entered as,\n'
                                    '    e.g., 2D5 or 2/3L7/9\n'
                                    '  * Wavelengths have to be entered in\n'
                                    '    nm, levels in cm^-1\n'
                                    '  * You can draw up to 5 colors per scheme,\n'
                                    '    that should be enough for a while :)\n'
                                    '  * Linebreaks: will put a linebreak between\n'
                                    '    the level and the term symbol.\n\n'
                                    'Questions?  trappitsch1@llnl.gov\n'
                                    'Complaints? isselhardt1@llnl.gov\n\n'
                                    'Version: 20180614')

    def quit(self):
        self.master.destroy()
        self.master.quit()


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


# run GUI
root = tk.Tk()
my_gui = RSD(root)
root.mainloop()
