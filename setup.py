from pysqlcipher3 import dbapi2 as sqlcipher
from tabulate import tabulate

#db = sqlcipher.connect('testing.db')
#db.execute('SELECT * FROM emails;')

password = ''
confirm = ''

print(tabulate([["Welcome to PassMan setup!"]], ["PassMan"], tablefmt="grid"))
print("\nWelcome to PassMan, you'll need to setup a master password!\n")

def createPassword():
    global password
    global confirm
    password = input("Password: ")
    confirm = input("Confirm: ")
    if password != confirm:
        print("Looks like your passwords don't match... Try again")
        createPassword()
    elif len(password) < 5:
        print("Your password seems short. You can make a new password or continue.")
        choice = input("Continue(Y/N): ")
        choice = choice.upper()
        if choice == 'N':
            createPassword()

createPassword()

set_password = "PRAGMA key='{}'".format(password)
print(set_password)

conn = sqlcipher.connect('testing.db')
cur = conn.cursor()
cur.execute(set_password)
#cur.execute("PRAGMA key='test'")
cur.execute("create table passwords (WEBSITE text, USERNAME text, PASSWORD text)")
cur.execute("""insert into passwords values ('gmail', 'testuser', 'MyPassword1#')""")
conn.commit()
cur.close()
