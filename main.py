import sys
import math
import PyQt5.QtWidgets as qt_widgets
from PyQt5 import uic
from PyQt5.QtCore import QLocale
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QDoubleValidator
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from vizualize import *
import pyvista as pv
import numpy as np

        
class MainUI(qt_widgets.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        uic.loadUi('main_menu.ui', self)
        self.vizualize_btn = self.findChild(qt_widgets.QPushButton, 'vizualize_button')
        self.vizualize_btn.clicked.connect(self.onVizualizeButtonClick)
        self.a_input = self.findChild(qt_widgets.QLineEdit, 'a_input')
        self.a_input.setValidator(QDoubleValidator(0.0, 100.0, 2, self).setLocale(QLocale("en_US")))
        self.b_input = self.findChild(qt_widgets.QLineEdit, 'b_input')
        self.b_input.setValidator(QDoubleValidator(0.0, 100.0, 2, self).setLocale(QLocale("en_US")))
        self.c_input = self.findChild(qt_widgets.QLineEdit, 'c_input')
        self.c_input.setValidator(QDoubleValidator(0.0, 100.0, 2, self).setLocale(QLocale("en_US")))
        
        self.show()
    
    def get_selected_color(self, number) -> None:
        r = self.findChild(qt_widgets.QRadioButton, number + "_color_r") 
        g = self.findChild(qt_widgets.QRadioButton, number + "_color_g") 
        b = self.findChild(qt_widgets.QRadioButton, number + "_color_b") 
        
        if r.isChecked():
            return "red"
        elif g.isChecked():
            return "green"
        elif b.isChecked():
            return "blue"
    
    def onVizualizeButtonClick(self):
        if len(self.a_input.text()) == 0 or len(self.b_input.text()) == 0 or len(self.c_input.text()) == 0:
            QMessageBox.about(self, "Ошибка", "Введите все значения!")
            return
        pos = (float(self.a_input.text()), float(self.b_input.text()), float(self.c_input.text())) 
        
        global viz_window 
        viz_window = VizualizeUI(pos=pos, color=self.get_selected_color("f"))
        viz_window.show()

if __name__ == '__main__':
    app= QApplication(sys.argv)
    main_window = MainUI()
    sys.exit(app.exec_())