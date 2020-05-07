# import bcrypt
#
# # from datetime import date
# password = 'linkgish'
# passw = password.encode('utf-8')
# salt = bcrypt.gensalt()
# hash = bcrypt.hashpw(passw, salt)
#
# print(passw)
# print(salt)
# print(hash)
#
# # today = date.today().isoformat()
# # print(today)

# import hashlib, os
#
# s = 'user'.encode('utf-8')
# salt = os.urandom(16)
# d = 'linkgish'.encode('utf-8')
# print(salt)
# print(hashlib.sha512(salt+d).hexdigest())

import hashlib, sqlite3, random, string
from datetime import datetime

def randomString(stringLength):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

dateToday = datetime.now()
username = 'razz'
email = "n.razif@gmail.com"
password = 'passwordddd'
passw = password.encode('utf-8')
salt = randomString(10).encode('utf-8')

hash = hashlib.sha512(salt+passw).hexdigest()

salt = salt.decode('utf-8')
hash = str(hash)

isActive = str(0)
print('Value is : ',username, email, salt, hash, dateToday, isActive)
conn = sqlite3.connect('AiDdatabase.db')
c = conn.cursor()
c.execute("SELECT username FROM Login_DB")
names = {name[0] for name in c.fetchall()}
if username in names:
    print("Username taken, break.")
else:
    insert_query = "INSERT INTO Login_DB \
                        (username, email, password_salt, password_hash, date_register, isActive) \
                        VALUES ('{}','{}','{}','{}','{}','{}')".format(username, email, salt, hash, dateToday, isActive)
    c = c.execute((insert_query))
    conn.commit()
    print("Done commit to database")

c.close()
