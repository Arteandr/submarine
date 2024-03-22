from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtGui import QCloseEvent
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
    modelName = "sup.stl"
    def __init__(self, pos, color):
        super(VizualizeUI, self).__init__()
        self.initUI()
        
        self.front_view = self.findChild(QtWidgets.QGroupBox, "front_view")
        self.front_view_l = self.findChild(QtWidgets.QVBoxLayout, "v_front_view") 
        front_interactor = SubmarineGLWidget(stl_file=self.modelName,
                                            pos=pos, 
                                            color=color, 
                                            parent=self.front_view,
                                            azimuth=90).get_widget()
        self.front_view_l.addWidget(front_interactor, stretch=1)
        
        self.back_view = self.findChild(QtWidgets.QGroupBox, "back_view")
        self.back_view_l = self.findChild(QtWidgets.QVBoxLayout, "v_back_view")
        back_interactor = SubmarineGLWidget(stl_file=self.modelName,
                                            pos=pos, 
                                            color=color, 
                                            parent=self.back_view,
                                            azimuth=270).get_widget()
        self.back_view_l.addWidget(back_interactor, stretch=1)
        
        self.global_view = self.findChild(QtWidgets.QGroupBox, "global_view")
        self.global_view_l= self.findChild(QtWidgets.QVBoxLayout, "v_global_view")
        global_interactor = SubmarineGLWidget(stl_file=self.modelName,
                                            pos=pos, 
                                            color=color, 
                                            parent=self.global_view,
                                            withAxes=True).get_widget()
        self.global_view_l.addWidget(global_interactor, stretch=1)
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        super().closeEvent(a0)
    def initUI(self):
        uic.loadUi('./vizualize.ui',self)
        
 
class SubmarineGLWidget(QtWidgets.QOpenGLWidget):
    start_pos = np.array([124,0,-4])
    crane_start_pos = np.array([50,-2,2])
    
    def __init__(self, stl_file, pos, color, parent, withAxes=False, azimuth=0):
        self.pos = pos 
        super().__init__()
        self.mesh = pv.read(stl_file)
        self.crane_mesh = pv.read('crane.stl')
        points = self.crane_mesh.points.copy()
        scaled_points = points * 1.5 + self.crane_start_pos
        self.crane_mesh.points = scaled_points
        self.pl = pvqt.QtInteractor(parent=parent)
        self.pl.camera_position = "xz"
        self.pl.camera.azimuth = azimuth
        
        end_point = self.get_endpoint() 
        
        length = np.linalg.norm(end_point - self.start_pos)
        direction = end_point - self.start_pos 
        direction /= np.linalg.norm(direction)
        
        line = pv.Line(tuple(self.start_pos.tolist()), tuple(end_point.tolist()))
        cyllinder = line.tube(radius=1)
        
        origin = np.array([0, 0, 0])
        x_axis_end = np.array([10000, 0, 0])
        y_axis_end = np.array([0, 10000, 0])
        z_axis_end = np.array([0, 0, 10000])

        x_line = pv.Line(origin, x_axis_end)
        y_line = pv.Line(origin, y_axis_end)
        z_line = pv.Line(origin, z_axis_end)
        
        
        self.pl.add_mesh(x_line, color='red')
        self.pl.add_mesh(y_line, color='green')
        self.pl.add_mesh(z_line, color='blue')
        self.pl.add_mesh(self.mesh, color='white')
        self.pl.add_mesh(self.crane_mesh, color='white')
        self.pl.add_mesh(cyllinder, color=color)
        self.rotate_crane()
        if withAxes:
            self.pl.add_axes()
            self.pl.grid = True
    
    def rotate_crane(self):
        axes = pv.Axes(show_actor=True, actor_scale=2.0, line_width=5)
        axes.origin = self.crane_start_pos
        self.pl.add_actor(axes.actor)
        self.crane_mesh.rotate_z(60, point=axes.origin, inplace=True)
        
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        super().closeEvent(a0)
        self.vtkWidget.Finalize()
        
    def get_endpoint(self): 
        x,y,z = self.pos
        pos_np = np.array([x,y,z])
        endpoint = pos_np + self.start_pos
        
        return endpoint

    def get_widget(self):
        return self.pl
    
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