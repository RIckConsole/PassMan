from pysqlcipher3 import dbapi2 as sqlcipher
from pyfiglet import Figlet
from getpass import getpass
import time
import pandas as pd
import qprompt

#BEGIN BANNER
f = Figlet(font='slant')
print(f.renderText('Pass Man'))
#END BANNER

print("Welcome to PassMan, please enter the master password to unlock.")
password = getpass()
pragma_input = "PRAGMA key='{}'".format(password)
attempts = 1

def testPassword():
    time.sleep(2)
    print("Wrong Password")
    global attempts
    print("Attempts: " + str(attempts))
    #password = getpass()
    #pragma_input = "PRAGMA key='{}'".format(password)
    try:
        password = getpass()
        pragma_input = "PRAGMA key='{}'".format(password)
        conn = sqlcipher.connect('testing.db')
        cur = conn.cursor()
        cur.execute(pragma_input)
        cur.execute('SELECT * FROM passwords;')
        conn.commit()
        #cur.close()
        #mainMenu()
    except:
        attempts = attempts + 1
        if attempts == 4:
            print("Maximum attempts met. Exiting...")
            exit()
        else:
            testPassword()

def searchByWebsite():
    global pragma_input
    query = qprompt.ask_str("Query")
    conn = sqlcipher.connect('testing.db')
    cur = conn.cursor()
    cur.execute(pragma_input)
    cur.execute("SELECT * FROM passwords WHERE WEBSITE LIKE '%{}%'".format(query))
    conn.commit()
    print(pd.read_sql_query("SELECT * FROM passwords WHERE WEBSITE LIKE '%{}%'".format(query), conn))
    cur.close()
    qprompt.pause()
    mainMenu()

def searchByUsername():
    global pragma_input
    query = qprompt.ask_str("Query")
    conn = sqlcipher.connect('testing.db')
    cur = conn.cursor()
    cur.execute(pragma_input)
    cur.execute("SELECT * FROM passwords WHERE USERNAME LIKE '%{}%'".format(query))
    conn.commit()
    print(pd.read_sql_query("SELECT * FROM passwords WHERE USERNAME LIKE '%{}%'".format(query), conn))
    cur.close()
    qprompt.pause()
    mainMenu()

def addPass():
    global pragma_input
    print("This will add a new set of credentials to the database.")
    website = qprompt.ask_str("Website")
    username = qprompt.ask_str("Username")
    password = qprompt.ask_str("Password")
    print("Here is what will be entered into the database:")
    print("Website: " + website)
    print("Username: " + username)
    print("Password: " + password)
    confirm = qprompt.ask_yesno(default="y")
    if confirm == False:
        addPass()
    else:
        conn = sqlcipher.connect('testing.db')
        cur = conn.cursor()
        cur.execute(pragma_input)
        cur.execute("INSERT INTO passwords values ('{}', '{}', '{}')".format(website, username, password))
        conn.commit()
        cur.close()
        print("Credentials added successfully!")
        qprompt.pause()
        mainMenu()

def sortWebsite():
    global pragma_input
    conn = sqlcipher.connect('testing.db')
    cur = conn.cursor()
    cur.execute(pragma_input)
    cur.execute("SELECT * FROM passwords ORDER BY WEBSITE")
    conn.commit()
    print(pd.read_sql_query("SELECT * FROM passwords ORDER BY WEBSITE", conn))
    cur.close()
    qprompt.pause()
    mainMenu()

def sortUsername():
    global pragma_input
    conn = sqlcipher.connect('testing.db')
    cur = conn.cursor()
    cur.execute(pragma_input)
    cur.execute("SELECT * FROM passwords ORDER BY USERNAME")
    conn.commit()
    print(pd.read_sql_query("SELECT * FROM passwords ORDER BY USERNAME", conn))
    cur.close()
    qprompt.pause
    mainMenu()

def listAll():
    global pragma_input
    conn = sqlcipher.connect('testing.db')
    cur = conn.cursor()
    cur.execute(pragma_input)
    cur.execute("SELECT * FROM passwords")
    conn.commit()
    print(pd.read_sql_query("SELECT * FROM passwords", conn))
    cur.close()
    qprompt.pause()
    mainMenu()

def sortMenu():
    menu = qprompt.Menu()
    menu.add("1", "Sort by website", sortWebsite)
    menu.add("2", "Sort by Username", sortUsername)
    menu.add("3", "List all passwords", listAll)
    menu.add("9", "Go back", mainMenu)
    menu.add("0", "Quit", exit)
    choice = menu.show(header="SORTING")

def mainMenu():
    menu = qprompt.Menu()
    menu.add("1", "Search by website", searchByWebsite)
    menu.add("2", "Search by username", searchByUsername)
    menu.add("3", "Add password", addPass)
    menu.add("4", "Remove password")
    menu.add("5", "Sort By...", sortMenu)
    menu.add("0", "Quit", exit)
    choice = menu.show()

try:
    conn = sqlcipher.connect('testing.db')
    cur = conn.cursor()
    cur.execute(pragma_input)
    cur.execute("SELECT * FROM passwords")
except:
    testPassword()
#inputPassword()
print("Successfully logged in!")
mainMenu()
