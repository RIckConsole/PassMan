from pysqlcipher3 import dbapi2 as sqlcipher
from tabulate import tabulate
from getpass import getpass

password = ''
confirm = ''

#BANNER
print(tabulate([["Welcome to PassMan setup!"]], ["PassMan"], tablefmt="grid"))
print("\nWelcome to PassMan, you'll need to setup a master password!\n")

def createPassword():
    global password
    global confirm
    password = getpass("Password: ")#Securely input password
    confirm = getpass("Confirm: ")  #Securely confirm
    if password != confirm:         #Testing for matching passwords
        print("Looks like your passwords don't match... Try again")
        createPassword()
    elif len(password) < 5:#testing for weak passwords
        print("Your password seems short. You can make a new password or continue.")
        choice = input("Continue(Y/N): ")
        choice = choice.upper()
        if choice == 'N':
            createPassword()

createPassword()

set_password = "PRAGMA key='{}'".format(password) #setup pragma_key value for DB encryption.

conn = sqlcipher.connect('testing.db')
cur = conn.cursor()
cur.execute(set_password) #sets password
#Creates table in DB with an ID, website, username, and password.
cur.execute("create table passwords (ID integer NOT NULL PRIMARY KEY, WEBSITE text, USERNAME text, PASSWORD text)")
#Creates example set of credentials for user
cur.execute("""insert into passwords (WEBSITE, USERNAME, PASSWORD) values ('gmail', 'testuser', 'MyPassword1#')""")
conn.commit()
cur.close()
