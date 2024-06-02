import sqlite3
import threading
import time

class DbHandler:
	def __init__(self):
		self.lock = threading.Lock()
		self.conn = sqlite3.connect('data.sqlite3', check_same_thread=False)
		self.conn.execute('PRAGMA journal_mode=WAL;')
		self.conn.execute('PRAGMA wal_autocheckpoint=1000;')
		self.conn.execute('''
			CREATE TABLE IF NOT EXISTS users (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT NOT NULL,
				age INTEGER NOT NULL
			)
		''')

	def insert(self, name: str, age: int):
		with self.lock:
			self.conn.execute('''
				INSERT INTO users (name, age)
				VALUES (?, ?)
			''', (name, age))
			self.conn.commit()

	def dispose(self):
		self.conn.close()


def print_with_delay(delay: float, *args):
	for e in args:
		time.sleep(delay)
		print(e)


def work(id: int, db: DbHandler):
	for i in range(1_000):
		db.insert(f'Thread {id}', i)


def main():
	db = DbHandler()
	start = time.time()

	threads = []
	for i in range(10):
		t = threading.Thread(target=work, args=(i, db))
		threads.append(t)
		t.start()

	for t in threads:
		t.join()

	end = time.time()
	elapsed = end - start
	print(f'Execution time: {format(elapsed, '.2f')} seconds')


if __name__ == '__main__':
	main()

# no WAL 						 = 32.82
# WAL autocheckpoint 			 = 8.89
# WAL autocheckpoint 1000		 = 8.91
# WAL autocheckpoint 500		 = 9.01
# WAL autocheckpoint 2000		 = 8.92
# WAL autocheckpoint 5			 = 14.70