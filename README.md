Included are two files: main_fixed.py and main_vul.py

To demonstrate SQL Injections, run main_vul.py
3 example attacks include:
- "OR 1=1; -- | in password field 
- hacker', 'none'); DELETE FROM users; -- | in the username field
- hacker', 'none'); UPDATE users SET pass = 'mine_now' WHERE user = 'admin'; -- | in username field
