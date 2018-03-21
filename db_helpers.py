import sqlite3
from collections import namedtuple

_db = "german.sqlite"

Word = namedtuple('Word', 'id, word, category')

def _connect():
	conn = sqlite3.connect(_db)
	c = conn.cursor()
	return conn, c
	

def create_table():
	conn, c = _connect()
	c.execute("""CREATE TABLE IF NOT EXISTS words(
		id integer primary key autoincrement,
		word text,
		category text)""")
	conn.commit()
	c.close()
	conn.close()

def get(category):
	conn, c = _connect()
	c.execute("SELECT id, word FROM words WHERE category = ?", (category,))
	words = [Word(id, word, category) for id, word in c.fetchall()]
	c.close()
	conn.close()
	return words

def add(word, category):
	conn, c = _connect()
	c.execute("INSERT INTO words (word, category) VALUES (?, ?)", (word, category))
	conn.commit()
	c.close()
	conn.close()
	
def remove(id):
	conn, c = _connect()
	c.execute("DELETE FROM words WHERE id = ?", (id,))
	conn.commit()
	c.close()
	conn.close()
