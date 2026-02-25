import sqlite3
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
cur.execute("UPDATE services_serviceprovider SET availability='not_available' WHERE id=1")
print('rows updated:', cur.rowcount)
conn.commit()
conn.close()
