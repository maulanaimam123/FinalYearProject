import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import os
# print(f'System path : {sys.path}')
sys.path.insert(1, os.getcwd())

from util.DrawingArea import DrawingArea
from util.MouseTracker import MouseTracker

class Window(QMainWindow):
    def __init__(self, title = None):
        super().__init__()
        self.title = title
        self.icon_dir = './icon/'
        self._initUI(title)
        self.show()

    def _initUI(self, title = None):
        self.setWindowTitle(title)
        self.resize(800, 500) # Default size
        self._center() # Move main window to the center
        self._setUpMenuBar() # Set up menu bar
        self._setUpWorkingSpace() # Set up default working space

    # MAIN WINDOW
    def _center(self):
        window_frame = self.frameGeometry()
        desktop_center = QDesktopWidget().availableGeometry().center()
        window_frame.moveCenter(desktop_center)
        self.move(window_frame.topLeft())

    def _setUpMenuBar(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('&File')
        # File --> Import image
        import_act = QAction(QIcon(self.icon_dir + 'open.png'), 'Import image...', self)
        import_act.setShortcut('Ctrl+O')
        import_act.triggered.connect(self.getImage)
        # File --> Save image
        save_act = QAction(QIcon(self.icon_dir + 'save.png'), 'Save image...', self)
        save_act.setShortcut('Ctrl+S')
        save_act.triggered.connect(self.saveImage)
        # File --> Exit
        exit_act = QAction(QIcon(self.icon_dir + 'exit.png'), 'Quit', self)
        exit_act.setShortcut('Ctrl+W')
        exit_act.triggered.connect(QApplication.instance().quit)
        # Compiling File menu
        file_menu.addActions([import_act, save_act, exit_act])

        # Analysis menu
        analysis_menu = menubar.addMenu('&Analysis')
        # Analysis --> Clear
        clear_act = QAction(QIcon(self.icon_dir + 'clear.png'), 'Clear image', self)
        clear_act.setShortcut('Ctrl+Q')
        clear_act.triggered.connect(self.clear)
        # Analysis --> Undo
        # Analysis --> Redo
        # Compiling Analysis menu
        analysis_menu.addActions([clear_act])
    
    def getImage(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File", "C:", "Image Files (*.jpg *.jpeg *.png)")
        self.DrawingArea.image_path = file_name[0]
        print(f'image path is {self.DrawingArea.image_path}')
        self.DrawingArea.loadImage()

    def saveImage(self):
        file_name = QFileDialog.getSaveFileName(self, caption = "Save file", directory = "C:", filter = "Image Files (*.jpg *.jpeg *.png)")
        self.DrawingArea.saveImage(file_name[0])
    
    def clear(self):
        self.DrawingArea.loadImage()
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Warning',
                            'Are you sure to quit?', QMessageBox.Yes |
                            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
    # WORKING SPACE
    def _setUpWorkingSpace(self):
        self.DrawingArea = DrawingArea(self)
        tracker = MouseTracker(self.DrawingArea)
        tracker.positionChanged.connect(self.on_position_changed)
        self.label_position = QLabel(self.DrawingArea, alignment=Qt.AlignCenter)
        self.label_position.setStyleSheet('background-color: white; border: 1px solid black; font: 14pt')

        # Central Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        lay = QVBoxLayout(main_widget)
        lay.addWidget(self.DrawingArea)
        lay.addWidget(QPushButton(QIcon(), 'Hellow World'))

    @pyqtSlot(QPoint)
    def on_position_changed(self, pos):
        delta = QPoint(30, -15)
        self.label_position.show()
        self.label_position.move(pos + delta)
        self.label_position.setText("(%d, %d)" % (pos.x(), pos.y()))
        self.label_position.adjustSize()

def main():
    app = QApplication(sys.argv)
    demo = Window('Some title...')
    demo.show()
    sys.exit(app.exec_())

main()