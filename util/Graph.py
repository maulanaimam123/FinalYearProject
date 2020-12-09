import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pyqtgraph as pg

class ScrollableGraph(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.scroll = QScrollArea()
        self.vbox = QVBoxLayout()

        self.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self)
        self.pen = pg.mkPen(color = (255, 0, 0), width = 3)

    def addProfile(self, profile):
        x = [i for i in range(1, len(profile) + 1)]
        plot_object = pg.PlotWidget()
        plot_object.setBackground('w')
        plot_object.plot(x, profile, pen = self.pen)
        self.vbox.addWidget(plot_object)

    def clear(self):
        for i in reversed(range(self.vbox.count())): 
            self.vbox.itemAt(i).widget().deleteLater()

            


# def main():
#     app = QApplication(sys.argv)
#     demo = ScrollableGraph()
#     demo.show()
#     sys.exit(app.exec_())

# main()