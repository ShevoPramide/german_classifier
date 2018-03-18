import sys
import time
from PyQt5.QtWidgets import *
import german_classifier_gui
import db_helpers

class MainWindow(QMainWindow, german_classifier_gui.Ui_MainWindow):
	def __init__(self, parent=None):
		super().__init__(parent=parent)
		self.setupUi(self)
		
		self.categories = ["Articles", "Animals", "Vegetables",
			"Simple Verbs", "Phrasal Verbs"]
		# self.data = dict.fromkeys(self.categories, [])
		self.category_combo.addItems(self.categories)
		
		self.submit_button.clicked.connect(self.add)
		
		self.tabWidget.currentChanged.connect(self.update_list)
		
		self.statusBar().setStyleSheet("color: mediumseagreen")
		

	def add(self):
		word = self.word_edit.text()
		category = self.category_combo.currentText()
		
		if not word:
			QMessageBox.warning(self, "Empty Field!",
					"You must enter a word to be categorized!")
			return
		
		if category == "Articles":
			article = word.partition(" ")[0]
			if article.lower() == "die":
				category = "die"
			elif article.lower() == "das":
				category = "das"
			elif article.lower() == "der":
				category = "der"
			else:
				QMessageBox.warning(self, "No valid article!",
					"This category requires `die`, `das` or `der` articles")
				return
		
		db_helpers.add(word, category)
		
		self.statusBar().showMessage("Word added successfully!", 1000)
		
	def update_list(self, index):
		category = self.tabWidget.tabText(index).replace('&', '')
		if category == "Articles": 
			die = db_helpers.get("die")
			self.die_list.clear()
			self.die_list.addItems(die)
			
			das = db_helpers.get("das")
			self.das_list.clear()
			self.das_list.addItems(das)
			
			der = db_helpers.get("der")
			self.der_list.clear()
			self.der_list.addItems(der)
			
		elif category == "Animals":
			animals = db_helpers.get("Animals")
			self.animal_list.clear()
			self.animal_list.addItems(animals)
			
		elif category == "Vegetables":
			vegetables = db_helpers.get("Vegetables")
			self.vegetable_list.clear()
			self.vegetable_list.addItems(vegetables)
			
		elif category == "Simple Verbs":
			simple_verbs = db_helpers.get("Simple Verbs")
			self.simple_list.clear()
			self.simple_list.addItems(simple_verbs)
			
		elif category == "Phrasal Verbs":
			phrasal_verbs = db_helpers.get("Phrasal Verbs")
			self.phrasal_list.clear()
			self.phrasal_list.addItems(phrasal_verbs)
		
		
		
if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec()
