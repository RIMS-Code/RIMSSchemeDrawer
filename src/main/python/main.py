from fbs_runtime.application_context.PyQt5 import ApplicationContext

from PyQt5.QtWidgets import QWidget, QMainWindow, QAction, QPushButton, QRadioButton, QCheckBox, QButtonGroup, \
    QTabWidget, QMessageBox, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QFileDialog
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.Qt import QSize
from PyQt5.QtGui import QFont, QDoubleValidator, QIntValidator, QIcon

import functools
import numpy as np
import sys
import plotter

class SchemeDrawer(QMainWindow):
    """
    RIMS scheme drawer, the PyQt5 version based on fbs

    Developer:  Reto Trappitsch, trappitsch1@llnl.gov
    Version:    2.0.0
    Date:       December 6, 2019
    """

    def __init__(self):
        # run in debug mode?
        self.rundebug = True

        # initialize the thing
        super().__init__()
        self.title = 'RIMS Scheme Drawer'
        self.left = 50
        self.top = 80
        self.width = 20
        self.height = 20

        # initialize the UI
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # settings:
        self.numberofsteps = 5
        self.lineedit_size = QSize(100, 20)

        # entries and labels necessary
        self.rbtngrp_units = QButtonGroup()
        self.rbtn_nm = QRadioButton('nm')
        self.rbtn_cm = QRadioButton('cm-1')
        self.lbl_steps = []
        self.edt_level = []
        self.edt_term = []
        self.edt_gslevel = QLineEdit()
        self.edt_gsterm = QLineEdit()
        self.edt_iplevel = QLineEdit()
        self.edt_ipterm = QLineEdit()
        self.chk_lowlying = []

        # settings line edits
        self.edt_sett_figwidth = QLineEdit('5')
        self.edt_sett_figheight = QLineEdit('8')
        self.edt_sett_fstitle = QLineEdit('14')
        self.edt_sett_fsaxes = QLineEdit('12')
        self.edt_sett_fsaxlbl = QLineEdit('14')
        self.chk_sett_linebreaks = QCheckBox('Line breaks?')
        self.edt_sett_fslbl = QLineEdit('12')
        self.edt_sett_headspace = QLineEdit('2000')
        self.edt_sett_arrwidth = QLineEdit('0.2')
        self.edt_sett_arrheadwidth = QLineEdit('0.6')
        self.edt_sett_preclambda = QLineEdit('3')
        self.edt_sett_preclevel = QLineEdit('0')
        self.rbtngrp_iplabel = QButtonGroup()
        self.rbtn_iplable_top = QRadioButton('Top')
        self.rbtn_iplable_bottom = QRadioButton('Bott.')
        self.edt_sett_plttitle = QLineEdit()

        # push buttons
        self.btn_plot = QPushButton('Plot')
        self.btn_save = QPushButton('Save')
        self.btn_test = QPushButton('Test')
        self.btn_help = QPushButton('Help')
        self.btn_quit = QPushButton('Quit')

        # main widget
        self.mainwidget = QWidget()
        self.setCentralWidget(self.mainwidget)

        # style forms
        self.fontheader = QFont()
        self.fontheader.setBold(True)

        # initialize the UI
        self.initUI()

        # set default values
        if self.rundebug:
            self.fill_default_values()

        # show the UI
        self.show()

    def initUI(self):
        """
        Initialize the UI
        """
        # bottom most row:
        bottomrowindex = 11   # depends on how many settings entries there are!
        if self.numberofsteps + 2 > bottomrowindex:
            bottomrowindex = self.numberofsteps + 2

        # define the grid layout
        layout = QGridLayout()   # columns

        # ### column 1: labels for states
        # radiobuttons for nm or cm-1
        self.rbtngrp_units.addButton(self.rbtn_nm)
        self.rbtngrp_units.addButton(self.rbtn_cm)
        # set default
        self.rbtn_nm.setChecked(True)
        # add to layout
        rbtn_layout = QHBoxLayout()
        rbtn_layout.addWidget(self.rbtn_nm)
        rbtn_layout.addStretch()
        rbtn_layout.addWidget(self.rbtn_cm)
        layout.addLayout(rbtn_layout, 0, 0, 1, 1)

        # headers for all
        # level
        lbl_level = QLabel('Level')
        lbl_level.setFont(self.fontheader)
        layout.addWidget(lbl_level, 0, 1, 1, 1)
        # term symbol
        lbl_trmsymb = QLabel('Term Symbol')
        lbl_trmsymb.setFont(self.fontheader)
        layout.addWidget(lbl_trmsymb, 0, 2, 1, 1)
        # ground state manifold?
        lbl_gsmani = QLabel('GS Manifold?')
        lbl_gsmani.setFont(self.fontheader)
        layout.addWidget(lbl_gsmani, 0, 3, 1, 1)
        # Settings
        lbl_sett = QLabel('Settings')
        lbl_sett.setFont(self.fontheader)
        layout.addWidget(lbl_sett, 0, 4, 1, 1)
        # plot title
        lbl_plttit = QLabel('Plot Title')
        lbl_plttit.setFont(self.fontheader)
        layout.addWidget(lbl_plttit, 0, 6, 1, 1)

        # ground state
        lbl_gs = QLabel('Ground state (cm<sup>-1</sup>)')
        layout.addWidget(lbl_gs, 1, 0, 1, 1)
        layout.addWidget(self.edt_gslevel, 1, 1, 1, 1)
        layout.addWidget(self.edt_gsterm, 1, 2, 1, 1)

        # individual steps
        for it in range(self.numberofsteps):
            stepnumb = it + 1
            # make label and append
            self.lbl_steps.append(QLabel())
            layout.addWidget(self.lbl_steps[it], 2 + it, 0, 1, 1)
            # level steps
            self.edt_level.append(QLineEdit())
            self.edt_level[it].setFixedSize(self.lineedit_size)
            self.edt_level[it].setValidator(QDoubleValidator())
            self.edt_level[it].setAlignment(Qt.AlignRight)
            layout.addWidget(self.edt_level[it], 2 + it, 1, 1, 1)
            # term symbol steps
            self.edt_term.append(QLineEdit())
            self.edt_term[it].setFixedSize(self.lineedit_size)
            layout.addWidget(self.edt_term[it], 2 + it, 2, 1, 1)
            # check boxes
            self.chk_lowlying.append(QCheckBox('Low-lying state?'))
            layout.addWidget(self.chk_lowlying[it], 2 + it, 3, 1, 1)
            self.chk_lowlying[it].toggled.connect(self.set_label_names)

        # name the labels
        self.set_label_names()

        # add IP label:
        ip_lbl = QLabel('IP (cm<sup>-1</sup>)')
        layout.addWidget(ip_lbl, 2 + len(self.lbl_steps), 0, 1, 1)
        layout.addWidget(self.edt_iplevel, 2 + len(self.lbl_steps), 1, 1, 1)
        layout.addWidget(self.edt_ipterm, 2 + len(self.lbl_steps), 2, 1, 1)

        # set sizes and validators of boxes defined outside loop
        self.edt_gslevel.setFixedSize(self.lineedit_size)
        self.edt_gslevel.setValidator(QDoubleValidator())
        self.edt_gslevel.setAlignment(Qt.AlignRight)
        self.edt_gsterm.setFixedSize(self.lineedit_size)
        self.edt_iplevel.setFixedSize(self.lineedit_size)
        self.edt_iplevel.setValidator(QDoubleValidator())
        self.edt_iplevel.setAlignment(Qt.AlignRight)
        self.edt_ipterm.setFixedSize(self.lineedit_size)

        # button group for ip label
        self.rbtngrp_iplabel.addButton(self.rbtn_iplable_top)
        self.rbtngrp_iplabel.addButton(self.rbtn_iplable_bottom)

        # labels for settings
        layout.addWidget(QLabel('Figure Width x Height:'), 1, 4, 1, 1)
        layout.addWidget(QLabel('Font size title:'), 2, 4, 1, 1)
        layout.addWidget(QLabel('Font size axes:'), 3, 4, 1, 1)
        layout.addWidget(QLabel('Font size axes label:'), 4, 4, 1, 1)
        layout.addWidget(QLabel('Font size labels:'), 5, 4, 1, 1)
        layout.addWidget(QLabel('Headspace (cm<sup>-1</sup>):'), 6, 4, 1, 1)
        layout.addWidget(QLabel('Arrow width:'), 7, 4, 1, 1)
        layout.addWidget(QLabel('Arrow head width:'), 8, 4, 1, 1)
        layout.addWidget(QLabel('Precision wavelength:'), 9, 4, 1, 1)
        layout.addWidget(QLabel('Precision level:'), 10, 4, 1, 1)
        layout.addWidget(QLabel('IP label position:'), 11, 4, 1, 1)
        # line edits and buttons
        tmplayout = QHBoxLayout()
        tmplayout.addWidget(self.edt_sett_figwidth)
        tmplayout.addStretch()
        tmplayout.addWidget(QLabel('x'))
        tmplayout.addStretch()
        tmplayout.addWidget(self.edt_sett_figheight)
        layout.addLayout(tmplayout, 1, 5, 1, 1)
        layout.addWidget(self.edt_sett_fstitle, 2, 5, 1, 1)
        layout.addWidget(self.edt_sett_fsaxes, 3, 5, 1, 1)
        layout.addWidget(self.edt_sett_fsaxlbl, 4, 5, 1, 1)
        layout.addWidget(self.chk_sett_linebreaks, 4, 6, 1, 1)
        layout.addWidget(self.edt_sett_fslbl, 5, 5, 1, 1)
        layout.addWidget(self.edt_sett_headspace, 6, 5, 1, 1)
        layout.addWidget(self.edt_sett_arrwidth, 7, 5, 1, 1)
        layout.addWidget(self.edt_sett_arrheadwidth, 8, 5, 1, 1)
        layout.addWidget(self.edt_sett_preclambda, 9, 5, 1, 1)
        layout.addWidget(self.edt_sett_preclevel, 10, 5, 1, 1)
        tmplayout = QHBoxLayout()
        tmplayout.addWidget(self.rbtn_iplable_top)
        tmplayout.addStretch()
        tmplayout.addWidget(self.rbtn_iplable_bottom)
        layout.addLayout(tmplayout, 11, 5, 1, 1)
        layout.addWidget(self.edt_sett_plttitle, 1, 6, 1, 1)
        
        # set sizes
        # self.edt_sett_figwidth.setFixedSize(self.lineedit_size)
        # self.edt_sett_figheight.setFixedSize(self.lineedit_size)
        # self.edt_sett_fstitle.setFixedSize(self.lineedit_size)
        # self.edt_sett_fsaxes.setFixedSize(self.lineedit_size)
        # self.edt_sett_fsaxlbl.setFixedSize(self.lineedit_size)
        # self.edt_sett_fslbl.setFixedSize(self.lineedit_size)
        # self.edt_sett_headspace.setFixedSize(self.lineedit_size)
        # self.edt_sett_arrwidth.setFixedSize(self.lineedit_size)
        # self.edt_sett_arrheadwidth.setFixedSize(self.lineedit_size)
        # self.edt_sett_preclambda.setFixedSize(self.lineedit_size)
        # self.edt_sett_preclevel.setFixedSize(self.lineedit_size)
        self.edt_sett_plttitle.setFixedSize(self.lineedit_size)
        # validators
        self.edt_sett_figwidth.setValidator(QDoubleValidator())
        self.edt_sett_figheight.setValidator(QDoubleValidator())
        self.edt_sett_fstitle.setValidator(QIntValidator())
        self.edt_sett_fsaxes.setValidator(QIntValidator())
        self.edt_sett_fsaxlbl.setValidator(QIntValidator())
        self.edt_sett_fslbl.setValidator(QIntValidator())
        self.edt_sett_headspace.setValidator(QDoubleValidator())
        self.edt_sett_arrwidth.setValidator(QDoubleValidator())
        self.edt_sett_arrheadwidth.setValidator(QDoubleValidator())
        self.edt_sett_preclambda.setValidator(QIntValidator())
        self.edt_sett_preclevel.setValidator(QIntValidator())
        # alignment
        self.edt_sett_figwidth.setAlignment(Qt.AlignCenter)
        self.edt_sett_figheight.setAlignment(Qt.AlignCenter)
        self.edt_sett_fstitle.setAlignment(Qt.AlignRight)
        self.edt_sett_fsaxes.setAlignment(Qt.AlignRight)
        self.edt_sett_fsaxlbl.setAlignment(Qt.AlignRight)
        self.edt_sett_fslbl.setAlignment(Qt.AlignRight)
        self.edt_sett_headspace.setAlignment(Qt.AlignRight)
        self.edt_sett_arrwidth.setAlignment(Qt.AlignRight)
        self.edt_sett_arrheadwidth.setAlignment(Qt.AlignRight)
        self.edt_sett_preclambda.setAlignment(Qt.AlignRight)
        self.edt_sett_preclevel.setAlignment(Qt.AlignRight)

        # push buttons
        layout.addWidget(self.btn_plot, 2, 6, 1, 1)
        layout.addWidget(self.btn_save, 3, 6, 1, 1)
        if self.rundebug:
            layout.addWidget(self.btn_test, bottomrowindex - 2, 6, 1, 1)
        layout.addWidget(self.btn_help, bottomrowindex - 1, 6, 1, 1)
        layout.addWidget(self.btn_quit, bottomrowindex, 6, 1, 1)

        # connect it all up
        self.rbtn_nm.toggled.connect(self.set_label_names)
        self.rbtn_cm.toggled.connect(self.set_label_names)
        # buttons
        self.btn_plot.clicked.connect(self.plot)
        self.btn_test.clicked.connect(self.test)
        self.btn_help.clicked.connect(self.help)
        self.btn_quit.clicked.connect(self.close)

        # set the layout to the widget
        self.mainwidget.setLayout(layout)

    def fill_default_values(self):
        """
        For testing
        """
        self.edt_level[0].setText('345.213')
        self.edt_level[1].setText('912.358')
        self.edt_level[2].setText('245.268')
        self.edt_gslevel.setText('0')
        self.edt_iplevel.setText('65000')

    def set_label_names(self):
        # get the unit
        unit = self.get_unit()
        # set the labels
        stepnumb = 0
        for it in range(self.numberofsteps):
            stepnumb += 1
            # appendix for step number in label
            app = 'th'
            if stepnumb == 1:
                app = 'st'
            elif stepnumb == 2:
                app = 'nd'
            elif stepnumb == 3:
                app = 'rd'
            # set the namestring according to if low lying is toggled or not
            if self.chk_lowlying[it].isChecked():
                stepnumb -= 1
                print(stepnumb)
                namestring = 'Low lying st '
            else:
                namestring = str(stepnumb) + app + ' step '
            # add unit
            namestring += '(' + unit + '):'
            self.lbl_steps[it].setText(namestring)

    def get_unit(self):
        """
        Returns the current unit
        :return unit:   <str>   'nm' or 'cm<sup>-1</sup>'
        """
        if self.rbtn_nm.isChecked():
            return 'nm'
        else:
            return 'cm<sup>-1</sup>'

    def plot(self):
        if self.rundebug:
            print('Plotting...')

    # buttons
    def help(self):
        if self.rundebug:
            print('Help pressed')

    def test(self):
        self.set_label_names()


if __name__ == '__main__':
    appctxt = ApplicationContext()
    ex = SchemeDrawer()
    exit_code = appctxt.app.exec_()  # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)