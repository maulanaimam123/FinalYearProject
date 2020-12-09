import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import random

class ScrollableGraph(QMainWindow):
    def __init__(self, drawing_area = None):
        super().__init__()
        self.drawing_area = drawing_area
        self.plotGraphs()
        self.initUI()

    def initUI(self):
        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

        for i in range(5):
            # object = QLabel("TextLabel")
            x = [1,2,3,4,5,6,7,8,9,10]
            y = [random.randint(20, 45) for _ in range(10)]
            object = pg.PlotWidget()
            object.setBackground('w')
            object.plot(x, y, pen = pg.mkPen(color = (255, 0, 0), width = 3))
            self.vbox.addWidget(object)

        self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        self.setGeometry(600, 100, 1000, 900)
        self.setWindowTitle('Scroll Area Demonstration')
        self.show()

    def plotGraphs(self):
        # Plotting intensity of lines
        # 1. Make sure that drawing_area is not Null
        if self.drawing_area is None:
            return
        lines = self.drawing_area.lines
        pen = pg.mkPen(color = (255, 0, 0), width = 3)
        for line in lines:
            graph = pg.PlotWidget()
            


def main():
    app = QApplication(sys.argv)
    demo = ScrollableGraph()
    demo.show()
    sys.exit(app.exec_())

main()