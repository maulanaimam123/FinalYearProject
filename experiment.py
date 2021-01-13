import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import random

class AlanPushButton(QPushButton):
    random_number = pyqtSignal(list, name = 'random number')
    a_signal = pyqtSignal()

    def __init__(self, parent):
        super(AlanPushButton, self).__init__(parent)
    
    def mousePressEvent(self, event):
        self.clicked()
        self.emitSignal()

    def emitSignal(self):
        self.a_signal.emit()

    def clicked(self):
        self.random_number.emit([i for i in range(random.randint(2,8))])


def window():
    app = QApplication(sys.argv)
    win = QDialog()

    b1 = AlanPushButton(win)
    b1.setText("Button1")
    b1.move(50,20)
    b1.random_number.connect(b1_clicked)
    b1.a_signal.connect(b1_signal)

    b2 = AlanPushButton(win)
    b2.setText("Button2")
    b2.move(50,50)
    # QObject.connect(b2, SIGNAL("random number"), b2_clicked)
    b2.random_number.connect(b2_clicked)

    win.setGeometry(100,100,200,100)
    win.setWindowTitle("PyQt")
    win.show()
    sys.exit(app.exec_())

@pyqtSlot(int)
def b1_clicked(num):
   print(f"Button 1 clicked, random number is {num}")

@pyqtSlot(int)
def b2_clicked(num):
   print(f"Button 2 clicked, random number is {num}")

@pyqtSlot()
def b1_signal():
    print('signal from b1 is emitted')

window()