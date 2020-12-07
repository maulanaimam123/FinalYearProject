from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class ScribbleArea(QWidget):
    """
      this scales the image but it's not good, too many refreshes really mess it up!!!
    """
    def __init__(self, parent=None):
        super(ScribbleArea, self).__init__(parent)

        self.setAttribute(Qt.WA_StaticContents)
        self.modified = False
        self.scribbling = False
        self.myPenWidth = 1
        self.myPenColor = Qt.blue
        # imageSize = QSize(500, 500)
        self.imagePath = './test image/SEMImage.png'
        self.image = QImage(self.imagePath)
        # self.image = QImage(imageSize, QImage.Format_RGB32)
        self.setFixedSize(self.image.width(), self.image.height())
        self.lastPoint = QPoint()
        self.lines = []

    def openImage(self, fileName):
        loadedImage = QImage(filename)
        # if not loadedImage.load(fileName):
        #     return False

        w = loadedImage.width()
        h = loadedImage.height()    
        self.mainWindow.resize(w, h)

#       newSize = loadedImage.size().expandedTo(self.size())
#       self.resizeImage(loadedImage, newSize)
        self.image = loadedImage
        self.modified = False
        self.update()
        return True

    def saveImage(self, fileName, fileFormat):
        visibleImage = self.image
        self.resizeImage(visibleImage, self.size())

        if visibleImage.save(fileName, fileFormat):
            self.modified = False
            return True
        else:
            return False

    def setPenColor(self, newColor):
        self.myPenColor = newColor

    def setPenWidth(self, newWidth):
        self.myPenWidth = newWidth

    def clearImage(self):
        # self.image.fill(qRgb(255, 255, 255))
        self.image = QImage(self.imagePath)
        self.modified = True
        self.update()

    def clearImageEntirely(self):
        self.lines = []
        # self.image.fill(qRgb(255, 255, 255))
        # self.image.loadFromData(self.imageData)
        # self.image.setOffset(QPoint())
        self.image = QImage(self.imagePath)
        self.modified = True
        self.update()

    def mousePressEvent(self, event):
#       print "self.image.width() = %d" % self.image.width()
#       print "self.image.height() = %d" % self.image.height()
#       print "self.image.size() = %s" % self.image.size()
#       print "self.size() = %s" % self.size()
#       print "event.pos() = %s" % event.pos()
        if event.button() == Qt.LeftButton:
            self.lastPoint = event.pos()
            self.scribbling = True

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.scribbling:
            self.clearImage()
            for line in self.lines:
                start, end = line
                self.drawLineTwoPoints(start, end)
            self.drawLineTo(event.pos())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.scribbling:
            self.drawLineTo(event.pos())
            self.scribbling = False
            self.lines.append((self.lastPoint, event.pos()))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(event.rect(), self.image)

    def resizeEvent(self, event):
#       print "resize event"
#       print "event = %s" % event
#       print "event.oldSize() = %s" % event.oldSize()
#       print "event.size() = %s" % event.size()

        self.resizeImage(self.image, event.size())

        if self.width() > self.image.width() or self.height() > self.image.height():
            newWidth = max(self.width() + 128, self.image.width())
            newHeight = max(self.height() + 128, self.image.height())
            # print "newWidth = %d, newHeight = %d" % (newWidth, newHeight)
            self.resizeImage(self.image, QSize(newWidth, newHeight))
            self.update()

        super(ScribbleArea, self).resizeEvent(event)

    def drawLineTo(self, endPoint):
        painter = QPainter(self.image)
        painter.setPen(QPen(self.myPenColor, self.myPenWidth,
            Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(self.lastPoint, endPoint)
        self.modified = True

        # rad = self.myPenWidth / 2 + 2
        # self.update(QRect(self.lastPoint, endPoint).normalized().adjusted(-rad, -rad, +rad, +rad))
        self.update()
        # self.lastPoint = QPoint(endPoint)
    
    def drawLineTwoPoints(self, startPoint, endPoint):
        painter = QPainter(self.image)
        painter.setPen(QPen(self.myPenColor, self.myPenWidth,
            Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(startPoint, endPoint)
        self.modified = True
        self.update()

    def resizeImage(self, image, newSize):
        if image.size() == newSize:
            return

#       print "image.size() = %s" % repr(image.size())
#       print "newSize = %s" % newSize

# this resizes the canvas without resampling the image
        newImage = QImage(newSize, QImage.Format_RGB32)
        newImage.fill(qRgb(255, 255, 255))
        painter = QPainter(newImage)
        painter.drawImage(QPoint(0, 0), image)


    # #  this resampled the image but it gets messed up with so many events...       
    # #      painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
    # #      painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        
    #     newImage = QImage(newSize, QImage.Format_RGB32)
    #     newImage.fill(qRgb(255, 255, 255))
    #     painter = QPainter(newImage)
    #     srcRect = QRect(QPoint(0,0), image.size())
    #     dstRect = QRect(QPoint(0,0), newSize)
    # #      print "srcRect = %s" % srcRect
    # #      print "dstRect = %s" % dstRect
    #     painter.drawImage(dstRect, image, srcRect)


        self.image = newImage

    def print_(self):
        printer = QPrinter(QPrinter.HighResolution)

        printDialog = QPrintDialog(printer, self)
        if printDialog.exec_() == QDialog.Accepted:
            painter = QPainter(printer)
            rect = painter.viewport()
            size = self.image.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.image.rect())
            painter.drawImage(0, 0, self.image)
            painter.end()

    def isModified(self):
        return self.modified

    def penColor(self):
        return self.myPenColor

    def penWidth(self):
        return self.myPenWidth


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.saveAsActs = []

        self.scribbleArea = ScribbleArea(self)
        self.scribbleArea.clearImage()
        self.scribbleArea.mainWindow = self  # maybe not using this?
        self.setCentralWidget(self.scribbleArea)

        self.createActions()
        self.createMenus()

        self.setWindowTitle("Scribble")
        self.resize(500, 500)

    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def open(self):
        if self.maybeSave():
            fileName = QFileDialog.getOpenFileName(self, "Open File",
                QDir.currentPath())
            if fileName:
                self.scribbleArea.openImage(fileName)

    def save(self):
        action = self.sender()
        fileFormat = action.data()
        self.saveFile(fileFormat)

    def penColor(self):
        newColor = QColorDialog.getColor(self.scribbleArea.penColor())
        if newColor.isValid():
            self.scribbleArea.setPenColor(newColor)

    def penWidth(self):
        newWidth, ok = QInputDialog.getInt(self, "Scribble",
            "Select pen width:", self.scribbleArea.penWidth(), 1, 50, 1)
        if ok:
            self.scribbleArea.setPenWidth(newWidth)

    def about(self):
        QMessageBox.about(self, "About Scribble",
            "<p>The <b>Scribble</b> example shows how to use "
            "QMainWindow as the base widget for an application, and how "
            "to reimplement some of QWidget's event handlers to receive "
            "the events generated for the application's widgets:</p>"
            "<p> We reimplement the mouse event handlers to facilitate "
            "drawing, the paint event handler to update the application "
            "and the resize event handler to optimize the application's "
            "appearance. In addition we reimplement the close event "
            "handler to intercept the close events before terminating "
            "the application.</p>"
            "<p> The example also demonstrates how to use QPainter to "
            "draw an image in real time, as well as to repaint "
            "widgets.</p>")

    def createActions(self):
        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O",
            triggered=self.open)

        for format in QImageWriter.supportedImageFormats():
            format = str(format)

            text = format.upper() + "..."

            action = QAction(text, self, triggered=self.save)
            action.setData(format)
            self.saveAsActs.append(action)

        self.printAct = QAction("&Print...", self,
            triggered=self.scribbleArea.print_)

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
            triggered=self.close)

        self.penColorAct = QAction("&Pen Color...", self,
            triggered=self.penColor)

        self.penWidthAct = QAction("Pen &Width...", self,
            triggered=self.penWidth)

        self.clearScreenAct = QAction("&Clear Screen", self,
            shortcut="Ctrl+L", triggered=self.scribbleArea.clearImageEntirely)

        self.aboutAct = QAction("&About", self, triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
            triggered=qApp.aboutQt)

    def createMenus(self):
        self.saveAsMenu = QMenu("&Save As", self)
        for action in self.saveAsActs:
            self.saveAsMenu.addAction(action)

        fileMenu = QMenu("&File", self)
        fileMenu.addAction(self.openAct)
        fileMenu.addMenu(self.saveAsMenu)
        fileMenu.addAction(self.printAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)

        optionMenu = QMenu("&Options", self)
        optionMenu.addAction(self.penColorAct)
        optionMenu.addAction(self.penWidthAct)
        optionMenu.addSeparator()
        optionMenu.addAction(self.clearScreenAct)

        helpMenu = QMenu("&Help", self)
        helpMenu.addAction(self.aboutAct)
        helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(fileMenu)
        self.menuBar().addMenu(optionMenu)
        self.menuBar().addMenu(helpMenu)

    def maybeSave(self):
        if self.scribbleArea.isModified():
            ret = QMessageBox.warning(self, "Scribble",
                "The image has been modified.\n"
                "Do you want to save your changes?",
                QMessageBox.Save | QMessageBox.Discard |
                QMessageBox.Cancel)
            if ret == QMessageBox.Save:
                return self.saveFile('png')
            elif ret == QMessageBox.Cancel:
                return False

        return True

    def saveFile(self, fileFormat):
        initialPath = QDir.currentPath() + '/untitled.' + fileFormat

        fileName = QFileDialog.getSaveFileName(self, "Save As",
            initialPath,
            "%s Files (*.%s);;All Files (*)" % (fileFormat.upper(), fileFormat))
        if fileName:
            return self.scribbleArea.saveImage(fileName, fileFormat)

        return False


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())