import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PIL.ImageQt import ImageQt
from PIL import Image
import numpy as np
import math

class DrawingArea(QWidget):
    loadSignal = pyqtSignal()
    profileSignal = pyqtSignal(list)

    def __init__(self):
        super(DrawingArea, self).__init__()

        self.image_path = None
        self.loadImage()

        self.drawing = False
        self.last_point = QPoint()
        self.lines = []
        self.profiles = []

        self.setUpPen()
    
    # Main drawing functionalities
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = event.pos()
            self.drawing = True

    def mouseMoveEvent(self, event):
        if self.drawing and (event.buttons() & Qt.LeftButton):
            self.updateImage()
            self.drawLineOnImage(self.last_point, event.pos())
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            self.image_lastdrawn = self.image.copy()
            self.drawing = False
            self.lines.append((self.last_point, event.pos()))
            self.extractLine()
            emit_value = [
                self.profiles[-1],
                self.lines[-1]
            ]
            self.profileSignal.emit(emit_value)

    # Auxilliary drawing functionalities
    def updateImage(self):
        self.image = self.image_lastdrawn.copy()
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

        # for line in self.lines:
        #     start, end = line
        #     painter.drawLine(start, end)

        self.update()

    def setUpPen(self, width = 5, color = 'orange'):
        self.pen = QPen(QColor(color), width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

    # Line profile functionalities
    def extractLine(self):
        start, end = self.lines[-1]
        x0, y0 = max(start.x(), 0), max(start.y(), 0)
        x1, y1 = min(end.x(), self.image_grayscale.shape[1] - 1), min(end.y(), self.image_grayscale.shape[0] - 1)
        num = int(np.hypot(x1-x0, y1-y0))
        rows, cols = np.linspace(y0, y1, num), np.linspace(x0, x1, num)
        profile = self.image_grayscale[rows.astype(np.int), cols.astype(np.int)]
        self.profiles.append(list(profile))

    # Other functionalities    
    def loadImage(self):
        # Unfix widget size
        self.setMaximumSize(QWIDGETSIZE_MAX,QWIDGETSIZE_MAX)
        self.setMinimumSize(0,0)

        # Load image
        # if self.image_path is None, create dummy image
        if self.image_path == None:
            self.image_grayscale = np.array(Image.new('L', (600, 400), 255))
            self.image = ImageQt(Image.new('RGB', (600, 400), (255, 255, 255)))
            self.image_lastdrawn = self.image.copy()

        else:
            # Store grayscale image to self.image_grayscale
            self.image_grayscale = np.array(Image.open(self.image_path).convert('L'))
            image = QImage(self.image_path)
            if image.isGrayscale():
                # Create RGB version using PIL
                image_rgb = Image.open(self.image_path).convert('RGB')

                # Store RGB version of image in self.image, self.image_original
                self.image = ImageQt(image_rgb)
                self.image_lastdrawn = self.image.copy()
                
            else:
                # Store original and drawn image as it is
                self.image = image
                self.image_lastdrawn = image.copy()

        # Refix widget size
        self.setFixedSize(self.image.width(), self.image.height())

        # Flush lines
        self.lines = []
        self.profiles = []
        self.loadSignal.emit()
        self.update()

    def saveImage(self, file_name):
        self.image.save(file_name, 'PNG', -1)

# def main():
#     app = QApplication(sys.argv)
    
#     demo = DrawingArea()
#     demo.show()

#     sys.exit(app.exec_())

# main()