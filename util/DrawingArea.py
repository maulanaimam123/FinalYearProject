import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class DrawingArea(QWidget):
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.image_path = './icon/default.jpg'
        self.image = QImage(self.image_path)
        self.setFixedSize(self.image.width(), self.image.height())

        self.drawing = False
        self.last_point = QPoint()
        self.lines = []

        self.setUpPen()
    
    # Main drawing functionalities
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = event.pos()
            self.drawing = True

    def mouseMoveEvent(self, event):
        if self.drawing and (event.buttons() & Qt.LeftButton):
            self.clearImage()
            for line in self.lines:
                start, end = line
                self.drawLineOnImage(start, end)
            self.drawLineOnImage(self.last_point, event.pos())
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            self.drawLineOnImage(self.last_point, event.pos())
            self.drawing = False
            self.lines.append((self.last_point, event.pos()))

    # Auxilliary drawing functionalities
    def clearImage(self):
        self.image = QImage(self.image_path)
        self.update()
    
    def drawLineOnImage(self, start, end):
        # Setting canvas
        painter = QPainter(self.image)
        painter.drawImage(self.rect(), self.image)
        painter.setPen(self.pen)

        # Draw line
        painter.drawLine(start, end)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(event.rect(), self.image)
        painter.setPen(self.pen)

        for line in self.lines:
            start, end = line
            painter.drawLine(start, end)

        self.update()

    def setUpPen(self, width = 5, color = 'orange'):
        self.pen = QPen(QColor(color), width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)


    # Other functionalities
    def refresh(self):
        # Unfix widget size
        self.setMaximumSize(QWIDGETSIZE_MAX,QWIDGETSIZE_MAX)
        self.setMinimumSize(0,0)

        # Load Image
        self.image = QImage(self.image_path)

        # Refix widget size
        self.setFixedSize(self.image.width(), self.image.height())

        # Flush lines
        self.lines = []
        self.update()


# def main():
#     app = QApplication(sys.argv)
#     demo = DrawingArea(app)
#     demo.show()
#     sys.exit(app.exec_())

# main()