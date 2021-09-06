# -*- coding: utf-8 -*-


import sys
import math
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


def rotation(x, y, m):
    return x * math.cos(-math.pi / m) - y * math.sin(-math.pi / m), x * math.sin(-math.pi / m) + y * math.cos(-math.pi / m)


class MyWidget(QWidget):
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._n = 0
        self.kind = "Kohh"
        self.resize(200, 150)
        self.__X = self.width() / 2
        self.__Y = self.height() / 2
        self.__R = min(self.__X, self.__Y) / 2    
    
    
    def wheelEvent(self, event):
        self.__R += event.angleDelta().y() / 8 / 7
        if self.__R < 0:
            self.__R = 0
        self.repaint()


    def mousePressEvent(self, event):
        self.__Xmouse = event.x()
        self.__Ymouse = event.y()
        self.__Xsaved = self.__X
        self.__Ysaved = self.__Y


    def mouseMoveEvent(self, event):
        self.__X = self.__Xsaved + event.x() - self.__Xmouse
        self.__Y = self.__Ysaved + event.y() - self.__Ymouse
        self.repaint()    
    
    def kind_K(self):
        self.kind = "Kohh"
        self.repaint()
        return
    
    def kind_L(self):
        self.kind = "Levi"
        self.repaint()
        return
    
    def kind_C(self):
        self.kind = "Cross"
        self.repaint()
        return    
    
        
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        n = self._n
        if self.kind == "Kohh":
            self.kohh(self.__X - self.__R, self.__Y + self.__R * 2 / 3, self.__X + self.__R, self.__Y + self.__R * 2 / 3, n, painter)
        elif self.kind == "Levi":
            self.levi(self.__X - self.__R * 2 / 3, self.__Y + self.__R, self.__X + self.__R * 2 / 3, self.__Y + self.__R, n, painter)
        elif self.kind == "Cross":
            self.cross(self.__X - self.__R, self.__Y, self.__X, self.__Y + self.__R, n, painter)
            self.cross(self.__X, self.__Y + self.__R, self.__X + self.__R, self.__Y, n, painter)
            self.cross(self.__X + self.__R, self.__Y, self.__X, self.__Y - self.__R, n, painter)
            self.cross(self.__X, self.__Y - self.__R, self.__X - self.__R, self.__Y, n, painter)
        painter.end()
    
    
    def kohh(self, x1, y1, x2, y2, n, painter):
        if n == 0:
            painter.drawLine(x1, y1, x2, y2)
            return
        else:
            x3, y3 = x1 + (x2 - x1) / 3, y1 + (y2 - y1) / 3
            x4, y4 = x2 - (x2 - x1) / 3, y2 - (y2 - y1) / 3
            x5, y5 = rotation(x4 - x3, y4 - y3, 3)
            x5 += x3
            y5 += y3
            return self.kohh(x1, y1, x3, y3, n - 1, painter), self.kohh(x3, y3, x5, y5, n - 1, painter), self.kohh(x5, y5, x4, y4, n - 1, painter), self.kohh(x4, y4, x2, y2, n - 1, painter)
    
    def levi(self, x1, y1, x2, y2, n, painter):
        if n == 0:
            painter.drawLine(x1, y1, x2, y2)
            return
        else:
            x3 = (x2 - x1) / 2
            y3 = (y2 - y1) / 2
            x3, y3 = rotation(x3, y3, 4)
            x3 = (2 ** 0.5) * x3 + x1
            y3 = (2 ** 0.5) * y3 + y1
            return self.levi(x1, y1, x3, y3, n - 1, painter), self.levi(x3, y3, x2, y2, n - 1, painter)
        
    
    def cross(self, x1, y1, x2, y2, n, painter):
        if n == 0:
            painter.drawLine(x1, y1, x2, y2)
            return
        else:
            x5, y5 = (x2 - x1) / 3 + x1, (y2 - y1) / 3 + y1
            x6, y6 = (x1 - x2) / 3 + x2, (y1 - y2) / 3 + y2            
            x3, y3 = (x2 - x1) / 3, (y2 - y1) / 3
            x3, y3 = rotation(x3, y3, 2)
            x3 += x5
            y3 += y5
            x4, y4 = (x1 - x2) / 3, (y1 - y2) / 3
            x4, y4 = rotation(x4, y4, -2)
            x4 += x6
            y4 += y6
            return self.cross(x1, y1, x5, y5, n - 1, painter), self.cross(x5, y5, x3, y3, n - 1, painter), self.cross(x3, y3, x4, y4, n - 1, painter), self.cross(x4, y4, x6, y6, n - 1, painter), self.cross(x6, y6, x2, y2, n - 1, painter)
        
        
    def setValue(self, val):
        self._n = val
        self.repaint()     
    
    
    def resize_ww(self, x, y):
        self.__X = self.__X * self.width() / x
        self.__Y = self.__Y * self.height() / y        


class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.resize(420, 200)
        self.setMinimumSize(420, 200)
        self.SpinBox = QSpinBox(self)
        self.SpinBox.setGeometry(10, 10, 100, 30)
        self.Widget = MyWidget(self)
        self.Widget.setGeometry(170, 10, 200, 150)
        self.Button1 = QRadioButton("Кривая Коха", self)
        self.Button2 = QRadioButton("Кривая Леви", self)
        self.Button3 = QRadioButton("Крест", self)
        self.Button1.setGeometry(10, 50, 120, 30)
        self.Button2.setGeometry(10, 90, 120, 30)
        self.Button3.setGeometry(10, 130, 120, 30)
        self.Button1.clicked.connect(self.Widget.kind_K)
        self.Button2.clicked.connect(self.Widget.kind_L)
        self.Button3.clicked.connect(self.Widget.kind_C)
        self.SpinBox.valueChanged.connect(self.Widget.setValue)
        self.__px = self.width() - 140
        self.__py = self.height() - 10
    
    def resizeEvent(self, event):
        self.Widget.setGeometry(135, 5, self.width() - 140, self.height() - 10)
        self.Widget.resize_ww(self.__px, self.__py)
        self.__px = self.width() - 140
        self.__py = self.height() - 10


app = QApplication(sys.argv)
Window = MyWindow()
Window.show()
app.exec_()