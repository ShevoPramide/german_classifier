import sys
from PyQt5.QtWidgets import *
import german_classifier_gui

class MainWindow(QMainWindow, german_classifier_gui.Ui_MainWindow):
	def __init__(self, parent=None):
		super().__init__(parent=parent)
		self.setupUi(self)
		
		
if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec()
