from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import random

class CustomPen(QPen):
    def __init__(self):
        width = 5
        super(CustomPen, self).__init__(QColor(), width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        self.randomizeColor()
    
    def generateRandomColor(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def randomizeColor(self):
        self.color_code = self.generateRandomColor()
        new_color = QColor(*self.color_code)
        self.setColor(new_color)