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
password = getpass() #Securely input master password
pragma_input = "PRAGMA key='{}'".format(password) #Sets up pragma key command with password input
attempts = 1 #initializes password attempts

def testPassword():
    global password
    global pragma_input
    time.sleep(2) #Sleep function to prevent brute force attempts
    print("Wrong Password")
    global attempts
    print("Attempts: " + str(attempts)) #show number of attempts
    try:
        global password
        global pragma_input
        password = getpass()
        pragma_input = "PRAGMA key='{}'".format(password)
        conn = sqlcipher.connect('.passman.db') #connect to database
        cur = conn.cursor() #create cursor
        cur.execute(pragma_input) #execute password input into database
        cur.execute('SELECT * FROM passwords;') #select contents of table to test for password error
        conn.commit()
        cur.close()
    except:
        attempts = attempts + 1 #add to attempts value if password fails
        if attempts == 4:
            print("Maximum attempts met. Exiting...") #exits program if max attempts reached
            exit()
        else:
            testPassword() #restart function if not at 4 attempts

def searchByWebsite():
    global pragma_input
    query = qprompt.ask_str("Query") #get query input from user
    conn = sqlcipher.connect('.passman.db')
    cur = conn.cursor()
    cur.execute(pragma_input)
    conn.commit()
    print(pd.read_sql_query("SELECT * FROM passwords WHERE WEBSITE LIKE '%{}%'".format(query), conn)) #select all records containing user input display it in a pretty way
    cur.close()
    qprompt.pause() #pause program and prompt user for continue
    mainMenu() #return to main menu

def searchByUsername():
    global pragma_input
    query = qprompt.ask_str("Query")
    conn = sqlcipher.connect('.passman.db')
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
    print("Website: " + website) #display information so user can confirm that it's correct
    print("Username: " + username)
    print("Password: " + password)
    confirm = qprompt.ask_yesno(default="y") #yes/no to confirm
    if confirm == False:
        retry = qprompt.ask_yesno("Would you like to retry?")
        if retry == False:
            mainMenu()
        else:
            addPass()
    else:
        conn = sqlcipher.connect('.passman.db')
        cur = conn.cursor()
        cur.execute(pragma_input)
        #add the users input into the database as a new set of credentials
        cur.execute("INSERT INTO passwords (WEBSITE, USERNAME, PASSWORD) values ('{}', '{}', '{}')".format(website, username, password))
        conn.commit()
        cur.close()
        print("Credentials added successfully!")
        qprompt.pause()
        mainMenu()

def updatePass():
    global pragma_input
    conn = sqlcipher.connect('.passman.db')
    cur = conn.cursor()
    cur.execute(pragma_input)
    print(pd.read_sql_query("SELECT * FROM passwords", conn))  #display all passwords so user can easily see its ID
    print("Select the ID of the credentials you wish to EDIT")
    try:
        ID = qprompt.ask_int("ID") #ask user for ID of credential to edit
    except:
        qprompt.error("ID NOT FOUND") #error if ID is not found
        retry = qprompt.ask_yesno("Retry?") #prompt user to retry or exit to main menu
        if retry == False:
            mainMenu()
        else:
            updatePass()

    print("Credential set selected! What would you like to change?") #ask user what about the chosen set of credentials they would like to change
    qprompt.alert("HINT: Use '?' for a list of options")
    selection = qprompt.ask_str("Edit", valid=["website", "username", "password"])
    if selection.lower() == "website":
        new = qprompt.ask_str("Enter new value")
        cur.execute("UPDATE passwords SET WEBSITE = '{}' WHERE ID = '{}'".format(new, ID)) #updates record with new info
    elif selection.lower() == "username":
        new = qprompt.ask_str("Enter new value")
        cur.execute("UPDATE passwords SET USERNAME = '{}' WHERE ID = '{}'".format(new, ID))
    elif selection.lower() == "password":
        new = qprompt.ask_str("Enter new value")
        cur.execute("UPDATE passwords SET PASSWORD = '{}' WHERE ID = '{}'".format(new, ID))
    conn.commit()
    cur.close()
    mainMenu()

def delPass():
    global pragma_input
    conn = sqlcipher.connect('.passman.db')
    cur = conn.cursor()
    cur.execute(pragma_input)
    print(pd.read_sql_query("SELECT * FROM passwords", conn))
    print("Select the ID of the credentials you wish to DELETE.")
    selection = qprompt.ask_int("ID")
    confirm = qprompt.ask_yesno(default="y")
    if confirm == False:
        print("Credential removal has been CANCELLED!")
        print()
        retry = qprompt.ask_yesno("Retry?", default="y")
        if retry == True:
            delPass()
        else:
            mainMenu()
    else:
        cur.execute("DELETE FROM passwords WHERE ID = '{}'".format(selection))
        print("Credentials deleted successfully!")
    conn.commit()
    cur.close()
    qprompt.pause()
    mainMenu()

def sortWebsite():
    global pragma_input
    conn = sqlcipher.connect('.passman.db')
    cur = conn.cursor()
    cur.execute(pragma_input)
    conn.commit()
    print(pd.read_sql_query("SELECT * FROM passwords ORDER BY WEBSITE", conn)) #orders all records by website
    cur.close()
    qprompt.pause()
    mainMenu()

def sortUsername():
    global pragma_input
    conn = sqlcipher.connect('.passman.db')
    cur = conn.cursor()
    cur.execute(pragma_input)
    conn.commit()
    print(pd.read_sql_query("SELECT * FROM passwords ORDER BY USERNAME", conn))
    cur.close()
    qprompt.pause
    mainMenu()

def listAll():
    global pragma_input
    conn = sqlcipher.connect('.passman.db')
    cur = conn.cursor()
    cur.execute(pragma_input)
    conn.commit()
    print(pd.read_sql_query("SELECT * FROM passwords", conn)) # lists all websites in ID order
    cur.close()
    qprompt.pause()
    mainMenu()

def sortMenu(): #submenu for choosing sort type
    menu = qprompt.Menu()
    menu.add("1", "Sort by website", sortWebsite) #params -> selection key, label, function to call once selected
    menu.add("2", "Sort by Username", sortUsername)
    menu.add("3", "List all passwords", listAll)
    menu.add("9", "Go back", mainMenu)
    menu.add("0", "Quit", exit)
    choice = menu.show(header="SORTING")

def mainMenu(): #main menu for function types
    menu = qprompt.Menu()
    menu.add("1", "Search by website", searchByWebsite)
    menu.add("2", "Search by username", searchByUsername)
    menu.add("3", "Add password", addPass)
    menu.add("4", "Remove password", delPass)
    menu.add("5", "Edit Password", updatePass)
    menu.add("6", "Sort By...", sortMenu)
    menu.add("0", "Quit", exit)
    choice = menu.show()

try:
    conn = sqlcipher.connect('.passman.db')
    cur = conn.cursor()
    cur.execute(pragma_input)
    cur.execute("SELECT * FROM passwords")
    conn.commit()
    cur.close()
except:
    testPassword()

print("Successfully logged in!")
mainMenu()
