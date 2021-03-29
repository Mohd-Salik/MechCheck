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

Notes:
data.insert("John", "A", "Jones", "0545841", "jones@gmail.com", "admin123", "doctor", "Pedetrician", "(8,118)")
data.insert("Tracey", "X", "Smith", "427887", "tracey@gmail.com", "admin123", "doctor", "Psychiatrist", "(12,109)")
data.insert("Anne", "E", "Rogers", "758716", "anne@gmail.com", "admin123", "doctor", "Dentist", "(11,105)")
data.insert("Kevin", "U", "Francis", "5564787", "francis@gmail.com", "user123", "user", "none", "(11,118)")
data.insert("Mary", "D", "Clark", "78524", "marry@gmail.com", "user123", "user", "Computer Scientist", "(10,111)")
data.insert("Jenny", "B", "Shaw", "75878", "jenny@gmail.com", "user123", "user", "Engineer", "(11,132)")
data.insert("Mark", "W", "Woods", "8757578", "mark@gmail.com", "user123", "user", "Janitor", "(9,114)")


PostsDB.insert({'email': 'jones@gmail.com', 'post': 'Did you know that the children of identical twins are genetically siblings rather than cousins? This is because they share 25% of their DNA. Full siblings share 50% of their DNA, half-siblings share 25%, and cousins share 12.5%. '})
PostsDB.insert({'email': 'anne@gmail.com', 'post': 'My heart goes out to the Malaysian people. This is such a tragedy. Words cant express how sad it is. I wish we could just have peace.'})
PostsDB.insert({'email': 'jones@gmail.com', 'post': 'Humans share 98.8% of their DNA with chimpanzees. But thankfully, despite this, the differences lie in how these genes are used. '})
PostsDB.insert({'email': 'tracey@gmail.com', 'post': 'I had a GREAT week, thanks to YOU! If you need anything, please reach out. #WorldSmileDay pic.twitter.com/ZpVmQPmcyc'})

Mindlog:
transfer find doctor to nav bar
/ create post wall on main screen
create post screen
users can delete their own post 
list all doctors
select specialization
create screen that displays profile