import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# Class for widget mouse tracking
class MouseTracker(QObject):
    positionChanged = pyqtSignal(QPoint)

    def __init__(self, widget):
        super().__init__(widget)
        self._widget = widget
        self.widget.setMouseTracking(True)
        self.widget.installEventFilter(self)

    @property
    def widget(self):
        return self._widget

    def eventFilter(self, o, e):
        if o is self.widget and e.type() == QEvent.MouseMove:
            self.positionChanged.emit(e.pos())
        return super().eventFilter(o, e)


class Example(QMainWindow):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.initUI(title)
    
    def initUI(self, title):
        # Main window set up
        self.resize(800,500)
        self.center()
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("lup.png"))

        # Menu bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')

        # Inside 'File' menu
        importAct = QAction(QIcon('open.png'), 'Import Image', self)
        importAct.setShortcut("Ctrl+O")
        importAct.setStatusTip("Load image")
        importAct.triggered.connect(self.getImage)

        exitAct = QAction(QIcon('exit.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(QApplication.instance().quit)

        # Compile menu bar
        fileMenu.addAction(importAct)
        fileMenu.addAction(exitAct)

        # Status bar - bottom of window
        self.statusBar()

        # Setting up working space
        self.Image = QLabel(self)
        self.Image.setStyleSheet("background-color: white; border: 1px solid black")
        self.Image.resize(600, 400)
        
        tracker = MouseTracker(self.Image)
        tracker.positionChanged.connect(self.on_positionChanged)

        self.label_position = QLabel(self.Image, alignment=Qt.AlignCenter)
        self.label_position.setStyleSheet('background-color: white; border: 1px solid black')

        # Setting Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        lay = QVBoxLayout(central_widget)
        lay.addWidget(self.Image)
        lay.addWidget(QLabel('Hellow world', self))
        self.resize(600,400)

        self.show()
    
    @pyqtSlot(QPoint)
    def on_positionChanged(self, pos):
        delta = QPoint(30, -15)
        self.label_position.show()
        self.label_position.move(pos + delta)
        self.label_position.setText("(%d, %d)" % (pos.x(), pos.y()))
        self.label_position.adjustSize()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Space:
            self.close()

    def getImage(self):
        fname = QFileDialog.getOpenFileName(self, "Open File", "C:", "Image Files (*.jpg *.jpeg *.png)")
        imagePath = fname[0]
        pixmap = QPixmap(imagePath)
        self.Image.setPixmap(QPixmap(pixmap))
        self.Image.resize(pixmap.width(), pixmap.height())
        
        self.resize(pixmap.width() + 100, pixmap.height() + 100)

    def buttonClick(self): # under construction....
        print(f'Button from {self.title} is clicked')

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Warning',
                            'Are you sure to quit?', QMessageBox.Yes |
                            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def main():
    app = QApplication(sys.argv)
    ex_a = Example("App 1")
    # ex_b = Example("App 2")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

