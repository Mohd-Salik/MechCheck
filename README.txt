REQUIREMENTS
-python
-kivy
-kivy_garden
-tinydb
-kivymd

DATABASE FORMAT

https://tinydb.readthedocs.io/en/latest/getting-started.html#installing-tinydb
first_name;middle_name;last_name  

# db.purge() DELETES ALL
# insert("Mark", "C", "Salik", "1234", "hen@gmail.com", "admin123", "Veterinarian", "(10,120)")
# search()
# print(db.all())
data = Database()
data.insert("John", "A", "Jones", "0545841", "jones@gmail.com", "admin123", "doctor", "Pedetrician", "(8,118)")
data.insert("Tracey", "X", "Smith", "427887", "tracey@gmail.com", "admin123", "doctor", "Psychiatrist", "(12,109)")
data.insert("Anne", "E", "Rogers", "758716", "anne@gmail.com", "admin123", "doctor", "Dentist", "(11,105)")

data.insert("Kevin", "U", "Francis", "5564787", "francis@gmail.com", "user123", "user", "none", "(11,118)")
data.insert("Mary", "D", "Clark", "78524", "marry@gmail.com", "user123", "user", "Computer Scientist", "(10,111)")
data.insert("Jenny", "B", "Shaw", "75878", "jenny@gmail.com", "user123", "user", "Engineer", "(11,132)")
data.insert("Mark", "W", "Woods", "8757578", "mark@gmail.com", "user123", "user", "Janitor", "(9,114)")


    MDRectangleFlatButton:
        text: 'Profile'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        on_press: root.manager.current = 'kv_profile'

MDFlatButton:
text: "UPDATE TEST"
on_press: app.updateUsername()
MDFlatButton:
text: "Find Doctors"
MDFlatButton:
text: "Settings"
MDFlatButton:
id: btn
text: "Logout" if btn.state == "normal" else "Logging out.."
background_color: 0.3, 0.4, 0.5, 1  
on_press: root.manager.current = 'kv_login'

                
                    MDFlatButton:
                        text: "UPDATE TEST"
                        on_press: app.updateUsername()
                    MDFlatButton:
                        text: "Find Doctors"
                    MDFlatButton:
                        text: "Settings"
                        background_color: 0.3, 0.4, 0.5, 1  
                        on_press: root.manager.current = 'kv_profile'
                    MDFlatButton:
                        text: "Logout"
                        background_color: 0.3, 0.4, 0.5, 1  
                        on_release: 
                            root.manager.current = 'kv_login'
                            root.manager.transition.direction = "right"

                    