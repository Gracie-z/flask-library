import sys
import os
sys.path.append('/Users/gracezhou/cs/python_flask/flask-library/hey')

from libraryweb.models import Book
from libraryweb import db
import pymysql
conn = pymysql.connect(host='localhost', user='root', database='library', passwd=os.environ.get('DB_PASSWORD'))
cur = conn.cursor()
cur.execute('USE library')
conn.commit()

def select_book(id):
    cur.execute('SELECT * FROM books WHERE id = %s',id)
    conn.commit()
    return cur.fetchone()
    

for i in range(1,100):
    name, author, id, pic_dir = select_book(i)
    book = Book(name=name, author=author, image_file=f'{str(i)}.jpg')
    db.session.add(book)
    db.session.commit()

cur.close()
conn.close()


