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
        rows, cols = 8, 4
        BW, BH, pad = 120, 30, 15
        winsize = ((1.5 + cols / 2) * pad + cols * BW,
                   (1.5 + rows / 2) * pad + rows * BH,
                   10, 10)  # width, height, xoffset, yoffset
        self.rows, self.cols = rows, cols
        self.BW, self.BH, self.pad = BW, BH, pad
        self.winsize = winsize

        # set master size
        master.geometry("%dx%d+%d+%d" % winsize)

        # font formatting
        self.font_std = tkFont.Font(size=11)
        self.font_bold = tkFont.Font(size=11, weight=tkFont.BOLD)
        self.font_ital = tkFont.Font(size=11, slant=tkFont.ITALIC)

        # Labels for the given steps (nm)
        self.step_title_label = tk.Label(master, text='Level', anchor=tk.W, font=self.font_bold)
        self.step_title_label.place(x=self.x(2), y=self.y(1), width=BW, height=BH)
        self.step1_label = tk.Label(master, text='1st step (nm):', anchor=tk.W, font=self.font_std)
        self.step2_label = tk.Label(master, text='2nd step (nm):', anchor=tk.W, font=self.font_std)
        self.step3_label = tk.Label(master, text='3rd step (nm):', anchor=tk.W, font=self.font_std)
        self.step4_label = tk.Label(master, text='4th step (nm):', anchor=tk.W, font=self.font_std)
        self.step5_label = tk.Label(master, text='5th step (nm):', anchor=tk.W, font=self.font_std)
        self.step1_label.place(x=self.x(1), y=self.y(3), width=BW, height=BH)
        self.step2_label.place(x=self.x(1), y=self.y(4), width=BW, height=BH)
        self.step3_label.place(x=self.x(1), y=self.y(5), width=BW, height=BH)
        self.step4_label.place(x=self.x(1), y=self.y(6), width=BW, height=BH)
        self.step5_label.place(x=self.x(1), y=self.y(7), width=BW, height=BH)

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

        # Title
        self.title_label = tk.Label(master, text='Plot Title', anchor=tk.W, font=self.font_bold)
        self.title_label.place(x=self.x(4), y=self.y(1), width=BW, height=BH)
        self.title_entry = tk.Entry(master)
        self.title_entry.place(x=self.x(4), y=self.y(2), width=BW, height=BH)

        # Buttons
        self.button_plot = tk.Button(master, text='Plot', font=self.font_std, command=self.plotter)
        self.button_save = tk.Button(master, text='Save', font=self.font_std, command=self.save)
        self.button_help = tk.Button(master, text='Help', font=self.font_std, command=self.help)
        self.button_quit = tk.Button(master, text='Quit', font=self.font_std, command=self.quit)
        self.button_plot.place(x=self.x(4), y=self.y(3), width=BW, height=BH)
        self.button_save.place(x=self.x(4), y=self.y(4), width=BW, height=BH)
        self.button_help.place(x=self.x(4), y=self.y(7), width=BW, height=BH)
        self.button_quit.place(x=self.x(4), y=self.y(8), width=BW, height=BH)

        # Options
        self.opt_linebreak_st = tk.IntVar()
        self.opt_linebreak = tk.Checkbutton(master, text='Linebreaks?', justify=tk.LEFT,
                                            variable=self.opt_linebreak_st, font=self.font_std)
        self.opt_linebreak.place(x=self.x(4), y=self.y(5), width=BW, height=BH)

        # fixme: temporary insert, remove later
        # self.step1_lambda.insert(tk.END, '273.448')
        # self.step2_lambda.insert(tk.END, '450.326')
        # self.step3_lambda.insert(tk.END, '820.357')
        # self.ip_value.insert(tk.END, '60003.')

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
        # let's first get the wavelengths that we want
        lambda1 = self.step1_lambda.get()
        lambda2 = self.step2_lambda.get()
        lambda3 = self.step3_lambda.get()
        lambda4 = self.step4_lambda.get()
        lambda5 = self.step5_lambda.get()
        lambda_steps = [lambda1, lambda2, lambda3, lambda4, lambda5]
        try:
            ipvalue = float(self.ip_value.get())
        except ValueError:
            messagebox.showerror('Enter IP', 'Please enter an ionization potential as a number and try again.')
            return
        # make lambda_steps into an np.array
        tmp = []
        for it in lambda_steps:
            try:
                tmp.append(float(it))
            except ValueError:
                break
        lambda_steps = np.array(tmp)

        # get the term symbols that were entered
        term_symb_entered = []
        term_symb_entered.append(self.term1.get())
        term_symb_entered.append(self.term2.get())
        term_symb_entered.append(self.term3.get())
        term_symb_entered.append(self.term4.get())
        term_symb_entered.append(self.term5.get())

        # get ground state wavenumber
        if self.ground_state_value.get() is '':
            wavenumber_gs = 0
        else:
            wavenumber_gs = float(self.ground_state_value.get())

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
            ymax = ipvalue + 2000.
        elif totwavenumber_photons + float(self.ground_state_value.get()) - ipvalue < 2000.:
            ymax = ipvalue + 2000.
        else:
            ymax = totwavenumber_photons + float(self.ground_state_value.get())

        # create term symbol string for direct usage in plotting
        term_symb = []
        for it in range(len(wavenumber_steps)):
            term_symb.append(term_to_string(term_symb_entered[it]))
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

        # create the figure
        f = Figure(figsize=(5, 8), dpi=100)
        a = f.add_subplot(111)
        # second axis for eV
        a2 = a.twinx()

        # shade the level above the IP
        xshade = [0., 10.]
        a.fill_between(xshade, ipvalue, ymax, facecolor='#adbbff', alpha=0.5)
        # label the IP
        if term_symb_ip is None:
            iplabelstr = 'IP, ' + str(round(ipvalue, 3)) + '$\,$cm$^{-1}$'
        else:
            iplabelstr = 'IP, ' + str(round(ipvalue, 3)) + '$\,$cm$^{-1}$' + lbreak + term_symb_ip
        a.text(textpad, ipvalue + 0.01*totwavenumber_photons, iplabelstr, color='k', ha='left')

        # Draw the vertical lines for every transition and IP, unless transition is above IP (shade area there)
        for it in transition_steps:
            if it < ipvalue:
                a.hlines(it, xmin=0, xmax=10)

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
            levelstr = str(round(wavenumber_gs, 3)) + '$\,$cm$^{-1}$'
        else:
            levelstr = str(round(wavenumber_gs, 3)) + '$\,$cm$^{-1}$' + lbreak + term_symb_gs

        a.text(10. - textpad, float(self.ground_state_value.get()), levelstr, color='k', ha='right', va='bottom')
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
            a.arrow(xval, yval_bott, 0, wstp, width=0.2, fc=col, ec=col, length_includes_head=True,
                    head_width=0.6, head_length=totwavenumber_photons/30.)

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
            lambdastr = str(round(lambda_steps[it], 3)) + '$\,$nm'
            a.text(xloc_lambda, tstp - wstp/2., lambdastr, color=col, ha=halignlam)

            # level text
            if term_symb[it] is None:
                levelstr = str(round(tstp, 3)) + '$\,$cm$^{-1}$'
            else:
                levelstr = str(round(tstp, 3)) + '$\,$cm$^{-1}$' + lbreak + term_symb[it]
            a.text(xloc_levelstr, tstp - 0.01*totwavenumber_photons, levelstr, color='k', ha=halignlev, va='top')

            # update yval_bott
            yval_bott = transition_steps[it]

        # Title:
        if self.title_entry is not '':
            a.set_title(self.title_entry.get())

        # ylabel
        a.set_ylabel('Wavenumber (cm$^{-1}$)')
        # axis limits
        a.set_xlim([0., 10.])
        a.set_ylim([0., ymax])

        # eV axis on the right
        a2.set_ylabel('Energy (eV)')
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
                                    'Version: 20180111')

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
