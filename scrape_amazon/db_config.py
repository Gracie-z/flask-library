
import pymysql

conn = pymysql.connect(host='localhost', user='root', database='library', passwd='Dfl1957n!!')
cur = conn.cursor()
cur.execute('USE library')
conn.commit()


def save_info(authors, book_name, pic_dir):
    cur.execute("INSERT INTO books (name, authors, pic_dir) VALUES (%s, %s, %s)"
                                                                    ,(book_name, authors, pic_dir))
    conn.commit()


def close_db():
    cur.close()
    conn.close() 

