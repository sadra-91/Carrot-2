from PyQt6.QtWidgets import QApplication,QWidget,QMainWindow
from PyQt6.QtGui import QIcon
import sys

app=QApplication(sys.argv)
self=QMainWindow()
self.showMaximized()
self.setWindowTitle("pfcarrot")
self.setWindowIcon(QIcon("carrot.png"))
self.setStyleSheet("background-color:#00011a")

self.show()

app.exec()