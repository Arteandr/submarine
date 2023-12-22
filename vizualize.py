from PyQt5.QtCore import Qt
from PyQt5 import uic
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtWidgets import QWidget
import numpy as np
import pyvista as pv
import pyvistaqt as pvqt
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class VizualizeUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(VizualizeUI, self).__init__()
        self.initUI()
        
        self.front_view = self.findChild(QtWidgets.QGroupBox, "front_view")
        self.front_view_l = self.findChild(QtWidgets.QVBoxLayout, "v_front_view") 
        front_interactor = SubmarineGLWidget('sup.stl',(200,0,100), 45, ("red","red"), self.front_view).get_widget()
        self.front_view_l.addWidget(front_interactor, stretch=1)
        
        self.back_view = self.findChild(QtWidgets.QGroupBox, "back_view")
        self.back_view_l = self.findChild(QtWidgets.QVBoxLayout, "v_back_view")
        back_interactor = SubmarineGLWidget('sup.stl',(200,0,100), 45, ("red","red"), self.back_view).get_widget()
        self.back_view_l.addWidget(back_interactor, stretch=1)
        
        self.global_view = self.findChild(QtWidgets.QGroupBox, "global_view")
        self.global_view_l= self.findChild(QtWidgets.QVBoxLayout, "v_global_view")
        global_interactor = SubmarineGLWidget('sup.stl',(200,0,100), 45, ("red","red"), self.global_view).get_widget()
        self.global_view_l.addWidget(global_interactor, stretch=1)
        
    def initUI(self):
        uic.loadUi('./vizualize.ui',self)
        
 
class SubmarineGLWidget(QtWidgets.QOpenGLWidget):
    start_pos = np.array([124,0,-4])
    
    def __init__(self, stl_file, pos, angle, colors, parent):
        fColor, sColor = colors
        self.pos = pos 
        self.angle = angle
        super().__init__()
        self.mesh = pv.read(stl_file)
        l1,l2 = self.draw_lines()
        #pl = pv.Plotter()
        self.pl = pvqt.QtInteractor(parent=parent)
        self.pl.add_mesh(self.mesh, color='white')
        self.pl.add_mesh(l1, color=fColor, line_width=5)
        self.pl.add_mesh(l2, color=sColor, line_width=5)
        self.pl.add_axes()
        #pl.show()
        
    def get_widget(self):
        return self.pl
    
    def draw_lines(self):
        endpoint = self.calculate_endpoint()
        topLine = pv.Line(tuple(self.start_pos.tolist()), endpoint)
        # end_point_second = self.start_pos + 100 * np.array([np.cos(-self.angle), 0, np.sin(-self.angle)])
        bottomLine = pv.Line(tuple(self.start_pos.tolist()), self.calculate_coordinates(endpoint))
        
        return (topLine, bottomLine)
    
    def calculate_coordinates(self, pos):
        x1,y1,z1 = pos
        angle_rad = math.radians(self.angle)
        z_offset = math.sin(angle_rad)
        z2 = z1 + z_offset
        print(z1)
        print(z2)
        
        return x1, y1, z2
    
    def calculate_endpoint(self):
        x,y,z = self.pos
        pos_np = np.array([x,y,z])
        end_point = pos_np + self.start_pos
        return tuple(end_point.tolist())
        

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslate(0.0, 0.0, -5.0)
        self.mesh.plot(opacity=1)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)