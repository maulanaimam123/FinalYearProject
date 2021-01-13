import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pyqtgraph as pg

class ScrollableGraph(QScrollArea):
    def __init__(self):
        super().__init__()
        self.penColor = (0, 0, 0) # Black by default
        self.initUI()

    def initUI(self):
        self.pen = pg.mkPen(color = self.penColor, width = 3)
        self.vbox = QVBoxLayout()
        main_widget = QWidget()
        main_widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(main_widget)

    def addProfile(self, profile, FWHM = 0):
        x = [i for i in range(1, len(profile) + 1)]
        plot_object = pg.PlotWidget(title = f'Beam FWHM is {FWHM} pixels' if FWHM != 0 else None)
        plot_object.setFixedHeight(150)
        plot_object.setBackground('w')
        plot_object.plot(x, profile, pen = pg.mkPen(color = self.penColor, width = 3))
        self.vbox.addWidget(plot_object)

    def clear(self):
        for i in reversed(range(self.vbox.count())): 
            self.vbox.itemAt(i).widget().deleteLater()

            


# def main():
#     app = QApplication(sys.argv)
    
#     demo = ScrollableGraph()
#     demo.show()
#     demo.addProfile([random.randint(0,10) for _ in range(20)])
#     demo.addProfile([random.randint(0,10) for _ in range(20)])
#     demo.addProfile([random.randint(0,10) for _ in range(20)])
#     demo.addProfile([random.randint(0,10) for _ in range(20)])

#     sys.exit(app.exec_())

# main()