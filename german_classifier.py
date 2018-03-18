#!/usr/bin/env python3
import sys
import time
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import german_classifier_gui
import db_helpers

class MainWindow(QMainWindow, german_classifier_gui.Ui_MainWindow):
	def __init__(self, parent=None):
		super().__init__(parent=parent)
		self.setupUi(self)
		
		self.categories = ["Articles", "Animals", "Vegetables",
			"Simple Verbs", "Phrasal Verbs"]
		self.category_combo.addItems(self.categories)
		
		self.submit_button.clicked.connect(self.add)
		
		self.tabWidget.currentChanged.connect(self.update_list)
		
		for lw in (self.der_list, self.die_list, self.das_list,
				self.animal_list, self.vegetable_list, self.simple_list,
				self.phrasal_list):			
			action = QAction('delete', self)
			action.triggered.connect(lambda _, lw=lw: self.remove(lw))
			lw.addAction(action)
			lw.setContextMenuPolicy(Qt.ActionsContextMenu)
		
		self.statusBar().setStyleSheet("color: mediumseagreen")
		
		self.setStyleSheet('''
			QMenu::item {
				color: black;
				background-color: white;
			}
			QMenu::item:selected {
				background-color: #2f8cc5;
				color: white;
			}
			''')
		

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
			for id, word, _ in die:
				item = QListWidgetItem(word)
				item.setData(Qt.UserRole, id)
				self.die_list.addItem(item)
			
			das = db_helpers.get("das")
			self.das_list.clear()
			for id, word, _ in das:
				item = QListWidgetItem(word)
				item.setData(Qt.UserRole, id)
				self.das_list.addItem(item)
			
			der = db_helpers.get("der")
			self.der_list.clear()
			for id, word, _ in der:
				item = QListWidgetItem(word)
				item.setData(Qt.UserRole, id)
				self.der_list.addItem(item)
			
		elif category == "Animals":
			animals = db_helpers.get("Animals")
			self.animal_list.clear()
			for id, word, _ in animals:
				item = QListWidgetItem(word)
				item.setData(Qt.UserRole, id)
				self.animal_list.addItem(item)
			
		elif category == "Vegetables":
			vegetables = db_helpers.get("Vegetables")
			self.vegetable_list.clear()
			for id, word, _ in vegetables:
				item = QListWidgetItem(word)
				item.setData(Qt.UserRole, id)
				self.vegetable_list.addItem(item)
			
		elif category == "Simple Verbs":
			simple_verbs = db_helpers.get("Simple Verbs")
			self.simple_list.clear()
			for id, word, _ in simple_verbs:
				item = QListWidgetItem(word)
				item.setData(Qt.UserRole, id)
				self.simple_list.addItem(item)
			
		elif category == "Phrasal Verbs":
			phrasal_verbs = db_helpers.get("Phrasal Verbs")
			self.phrasal_list.clear()
			for id, word, _ in phrasal_verbs:
				item = QListWidgetItem(word)
				item.setData(Qt.UserRole, id)
				self.phrasal_list.addItem(item)
		
	def remove(self, lw):
		# delete from the list widget
		row = lw.currentRow()
		if row == -1: return	# in case of empty list
		item = lw.takeItem(row)
		
		# delete from the database
		id = item.data(Qt.UserRole)
		# run the removal operation in another thread, to avoid unexplained delay!
		threading.Thread(target=lambda: db_helpers.remove(id)).start()
		
		
		
if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec()
