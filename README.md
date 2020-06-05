# PassMan
PassMan is a simple password manager written in python. It uses sqlcipher to encrypt the database. 

## Features
- Sqlcipher encrypted database with a master password
- Intuitive CLI menu
- Ability to search for, sort by, add/remove, and update/edit online credentials.

## Usage

Install the requirements (Requires Python 3 or above)

``` sh
pip install -r requirements.txt
```

Run the setup script to create your master password and the encrypted database.
``` sh
python setup.py
```
Then run the PassMan.py script to login to your database.

``` sh
python PassMan.py
```

Gives 3 attempts for the correct login password or program will exit.
The simple CLI menu will help you navigate and manage your credentials.

## Functions
 - Search By Website
    + Enter the name of a website (takes any string) and filter results to show credentials with websites containing that string
 - Search By Username
    + Enter a username (takes any string) and filter results to show credentials with usernames containing that string
 - Add Crededentials
    + Displays a menu to first add a website, then a username, and finally a password to insert into the database
    + Automatically assigns a unique ID to the credential
    + Password is encrypted when it is added to the database
 - Delete Crededentials
    + Lists all credentials with their unique ID
    + Deletes a credential from the database by selecting its ID
    + Confirmation that credential will be deleted
 - Update Credentials
    + Lists all credentials with their unique ID
    + Choose a credential by selecting its ID
    + Displays prompt to choose to update a website, username, or password
    + Type '?' in prompt for list of available options
    - Update Website
        + Displays a prompt to update the website for that specific credential
    - Update Username
        + Displays a prompt to update the username for that specific credential
    - Update Password
        + Displays a prompt to update the password for that specific credential
 - List Credentials
    + Displays list of all credentials ordered by their ID
 - Sort Credentials
    + Displays list of all credentials ordered by website or username based on user selection
