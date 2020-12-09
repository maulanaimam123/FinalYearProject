import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.title = "Image Viewer"
        self.setWindowTitle(self.title)

        label = QLabel(self)
        img = QImage(QSize(400, 300), QImage.Format_Grayscale8)
        painter = QPainter(img)
        painter.fillRect(QRectF(0,0,400,300), QColor('green'))
        c = img.pixel(100, 100)
        colors = QColor(c).get
        print(f'is img grayscale? {img.isGrayscale()}')
        print(f'pixel value at 100,100 : {colors}')
        del painter



        label.setPixmap(QPixmap.fromImage(img))
        self.setCentralWidget(label)
        self.resize(img.width(), img.height())


app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())