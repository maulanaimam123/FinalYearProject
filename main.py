import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import os
sys.path.insert(1, os.getcwd())

from util.DrawingArea import DrawingArea
from util.MouseTracker import MouseTracker
from util.Graph import ScrollableGraph
from util.CustomPen import CustomPen
from util.algorithm import calculate_beam_diameter

class Window(QMainWindow):
    def __init__(self, title = None):
        super().__init__()
        self.title = title
        self.icon_dir = './icon/'
        self.show()
        self.pen = CustomPen()
        self._initUI(title)

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
        file_name = QFileDialog.getOpenFileName(self, "Open File", "./", "Image Files (*.jpg *.jpeg *.png)")
        self.DrawingArea.image_path = file_name[0]
        self.DrawingArea.loadImage()

    def saveImage(self):
        file_name = QFileDialog.getSaveFileName(self, caption = "Save file", directory = "./", filter = "Image Files (*.jpg *.jpeg *.png)")
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
        # Drawing Area
        self.DrawingArea = DrawingArea()
        self.DrawingArea.pen = self.pen

        # Connecting Signal from DrawingArea
        self.DrawingArea.profileSignal.connect(self.add_graph)
        self.DrawingArea.loadSignal.connect(self.refresh_plot)

        # Mouse Tracker
        tracker = MouseTracker(self.DrawingArea)

        # Connecting Signal from MouseTracker
        tracker.positionChanged.connect(self.on_position_changed)
        self.label_position = QLabel(self.DrawingArea, alignment=Qt.AlignCenter)
        self.label_position.setStyleSheet('background-color: white; border: 1px solid black; font: 14pt')

        # Profiles Plot
        self.ProfilePlot = ScrollableGraph()
        self.ProfilePlot.setFixedWidth(400)

        # Central Layout
        firstRowWidget = QWidget()
        firstRowLayout = QHBoxLayout(firstRowWidget)
        firstRowLayout.addWidget(self.DrawingArea)
        firstRowLayout.addWidget(self.ProfilePlot)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        lay = QVBoxLayout(main_widget)

        lay.addWidget(firstRowWidget)
        lay.addWidget(QPushButton(QIcon(), 'Hellow World'))

    # SIGNAL HANDLING
    @pyqtSlot(QPoint)
    def on_position_changed(self, pos):
        delta = QPoint(30, -15)
        self.label_position.show()
        self.label_position.move(pos + delta)
        self.label_position.setText("(%d, %d)" % (pos.x(), pos.y()))
        self.label_position.adjustSize()

    @pyqtSlot(list)
    def add_graph(self, values):
        profile, line_coords = values 
        self.ProfilePlot.penColor = self.pen.color_code
        self.ProfilePlot.addProfile(profile)
        FWHM, first_derivative = calculate_beam_diameter(profile, 
                                                         line_coords,
                                                         self.DrawingArea.image_grayscale.shape[1],
                                                         self.DrawingArea.image_grayscale.shape[0])
        self.ProfilePlot.addProfile(first_derivative, FWHM = FWHM)
        self.pen.randomizeColor()
    
    @pyqtSlot()
    def refresh_plot(self):
        self.ProfilePlot.clear()

def main():
    app = QApplication(sys.argv)
    demo = Window('SEM Image Analysis')
    demo.show()
    sys.exit(app.exec_())

main()