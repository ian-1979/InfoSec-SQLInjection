import sqlite3
from tkinter import *
from tkinter import ttk


# create and link database
file = "scheetzDB.db"
db = sqlite3.connect(file)
cr = db.cursor()

def init_db():
	# create database and table
	cr.execute('''CREATE TABLE IF NOT EXISTS users(user text, pass text)''')
	db.commit()
	# create existing login info
	cr.execute(f"INSERT INTO users VALUES ('admin', 'complexPassword123')")
	cr.execute(f"INSERT INTO users VALUES ('normal user', 'simple')")


# Main Window
root = Tk()
frame = ttk.Frame(root, padding=10)
frame.grid()

init_db()

# login variables
userVar=StringVar()
passVar=StringVar()

# checks if info matches table data
def login():
	if check_valid() == True:
		if check_table() == True:
			suc_window("Login Successful!")
		else:
			err_window("Login Failed")

# checks if entered info is already in table
def check_table():
	inUser = userVar.get()
	inPass = passVar.get()
	# vulnerable to "OR 1=1; -- in password field
	cr.execute('SELECT * from users WHERE user="%s" AND pass="%s"' % (inUser, inPass))
	if not cr.fetchall():
		return False
	else:
		return True

# checks if data is not already in table, if not, adds data
def register_info():
	if check_valid() == True:
		if check_table() == False:
			inUser = userVar.get()
			inPass = passVar.get()
			# vulnerable to hacker', 'none'); DELETE FROM users; --
			# vulnerable to hacker', 'none'); UPDATE users SET pass = 'mine_now' WHERE user = 'admin'; --
			cr.executescript(f"INSERT INTO users VALUES ('{inUser}', '{inPass}')")
			db.commit()
			suc_window("Account created succesfully!")
		else:
			err_window("User credidentials already exist!")
			

# checks if info is valid input
def check_valid():
	if userVar.get() == "":
		err_window("Username field cannot be left empty")
	if passVar.get() == "":
		err_window("Password field cannot be left empty")
	else:
		return(True)


# Error Window
def err_window(errText):
	err = Tk()
	errF = ttk.Frame(err, padding=10)
	errF.grid()
	ttk.Label(errF, text=errText).grid(column=0, row=0)
	ttk.Button(errF, text="Okay", command=err.destroy).grid(column=0, row=1)

# Success Window
def suc_window(message):
	suc = Tk()
	sucF = ttk.Frame(suc, padding=10)
	sucF.grid()
	ttk.Label(sucF, text=message).grid(column=0, row=0)
	ttk.Button(sucF, text="Okay", command=suc.destroy).grid(column=1, row=0)

# Window Labels
ttk.Label(frame, text="Username: ").grid(column=0, row=0)
ttk.Label(frame, text="Password: ").grid(column=0, row=1)

# Entry Boxes
userEnt = ttk.Entry(frame, textvariable = userVar).grid(column=1, row=0)
passEnt = ttk.Entry(frame, textvariable = passVar).grid(column=1, row=1)

# Window Buttons
ttk.Button(frame, text="Login", command=login).grid(column=0, row=3)
ttk.Button(frame, text="Sign Up", command=register_info).grid(column=1, row=3)
ttk.Button(frame, text="Quit", command=root.destroy).grid(column=2, row=3)

root.mainloop()