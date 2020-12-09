import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PIL.ImageQt import ImageQt
from PIL import Image

class DrawingArea(QWidget):
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent

        self.image_path = None
        self.loadImage()

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
            self.updateImage()
            self.drawLineOnImage(self.last_point, event.pos())
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            self.image_lastdrawn = self.image.copy()
            self.drawing = False
            self.lines.append((self.last_point, event.pos()))

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

        for line in self.lines:
            start, end = line
            painter.drawLine(start, end)

        self.update()

    def setUpPen(self, width = 5, color = 'orange'):
        self.pen = QPen(QColor(color), width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)


    # Other functionalities    
    def loadImage(self):
        # Unfix widget size
        self.setMaximumSize(QWIDGETSIZE_MAX,QWIDGETSIZE_MAX)
        self.setMinimumSize(0,0)

        # Load image
        # if self.image_path is None, create dummy image
        if self.image_path == None:
            self.image_grayscale = ImageQt(Image.new('L', (600, 400), 255))
            self.image = ImageQt(Image.new('RGB', (600, 400), (255, 255, 255)))
            self.image_lastdrawn = self.image.copy()

        else:
            image = QImage(self.image_path)
            if image.isGrayscale():

                # Store grayscale image to self.image_grayscale
                self.image_grayscale = image

                # Create RGB version using PIL
                image_rgb = Image.open(self.image_path).convert('RGB')

                # Store RGB version of image in self.image, self.image_original
                self.image = ImageQt(image_rgb)
                self.image_lastdrawn = self.image.copy()
                
            else:
                # Create grayscale version --> self.image_grayscale
                image_gray = Image.open(self.image_path).convert('L')
                self.image_grayscale = ImageQt(image_gray)

                # Store original and drawn image as it is
                self.image = image
                self.image_lastdrawn = image.copy()

        # Refix widget size
        self.setFixedSize(self.image.width(), self.image.height())

        # Flush lines
        self.lines = []
        self.update()

    def saveImage(self, file_name):
        self.image.save(file_name, 'PNG', -1)

# def main():
#     app = QApplication(sys.argv)
#     demo = DrawingArea(app)
#     demo.show()
#     sys.exit(app.exec_())

# main()