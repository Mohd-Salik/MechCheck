# MechCheck
v1.2

REQUIREMENTS
-python
-kivy
-kivy_garden
-tinydb
-kivymd

https://tinydb.readthedocs.io/en/latest/getting-started.html#installing-tinydb

UpdateLog:
-Completed Location Feature

# Create table
cur.execute('''CREATE TABLE userstb
            (fname text, mname text, lname text, contact text, email text, pass text, doctor boolean, profession text, maploc text)''')
cur.execute("INSERT INTO userstb VALUES ('Mark','M','Riddle', '09052774814', 'doctor@gmail', 'doctor', true, 'opthalmologist', '[0.41, 123.88]')")
cur.execute("INSERT INTO userstb VALUES ('Kelly','G','Theadmin', '0902274833', 'Kelly@gmail', 'pass2', true, 'Pedetrician', '[0.42, 122.88]')")
cur.execute("INSERT INTO userstb VALUES ('Rick','L','Grimes', '0556991142', 'Rick@gmail', 'pass3', true, 'Dermatologist', '[0.40, 120.88]')")
cur.execute("INSERT INTO userstb VALUES ('Bryan','M','Theuser', '0902274833', 'user@gmail', 'user', false, 'ComputerScience', '[0.43, 123.88]')")
userdb.commit()

cur.execute('''CREATE TABLE poststb
            (email text, post text)''')
cur.execute("INSERT INTO poststb VALUES ('Rick@gmail','Did you know that the children of identical twins are genetically siblings rather than cousins? This is because they share 25% of their DNA')")
cur.execute("INSERT INTO poststb VALUES ('Kelly@gmail','My heart goes out to the Malaysian people. This is such a tragedy. Words cant express how sad it is.')")
cur.execute("INSERT INTO poststb VALUES ('Rick@gmail','Humans share 98.8% of their DNA with chimpanzees. But thankfully, despite this, the differences lie in how these genes are used. ')")
cur.execute("INSERT INTO poststb VALUES ('Kelly@gmail','I had a GREAT week, thanks to YOU! ')")

userdb.commit()

to continute:
>submit booking to db
>open my booking page, for user see my books, for doctor manage request books
>my profile (just show profile no edit yet)

padding: [0, 0, 0, 0]
[padding_left, padding_top, padding_right, padding_bottom].

missing validation in createAccountDB