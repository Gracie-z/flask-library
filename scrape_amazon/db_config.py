
import pymysql
import os

conn = pymysql.connect(host='localhost', user='root', database='library', passwd=os.environ.get('DB_PASSWORD'))
cur = conn.cursor()
cur.execute('USE library')
conn.commit()


def save_info(authors, book_name, pic_dir):
    cur.execute("INSERT INTO books (name, authors, pic_dir) VALUES (%s, %s, %s)"
                                                                    ,(book_name, authors, pic_dir))
    conn.commit()
def select_book(id):
    cur.execute('SELECT * FROM books WHERE id = %s',id)
    return cur.fetchone()

def close_db():
    cur.close()
    conn.close() 
