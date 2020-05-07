import bcrypt

# from datetime import date
password = 'linkgish'
passw = password.encode('utf-8')
salt = bcrypt.gensalt()
hash = bcrypt.hashpw(passw, salt)

print(passw)
print(salt)
print(hash)

# today = date.today().isoformat()
# print(today)