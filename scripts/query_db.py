import sqlite3
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
print('AUTH_USER rows:')
for row in cur.execute('SELECT id, username, email, first_name, last_name FROM auth_user'):
    print(row)
print('\nSERVICE_PROVIDER rows:')
for row in cur.execute('SELECT id, name, email, user_id FROM services_serviceprovider'):
    print(row)
print('\nBOOKING rows:')
for row in cur.execute('SELECT id, provider_id, customer_user_id, customer_name, status FROM services_booking'):
    print(row)
conn.close()
