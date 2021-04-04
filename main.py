import math, sqlite3
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.label import MDLabel
from kivymd.uix.button import Button, MDRoundFlatButton
from kivymd.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarListItem, ThreeLineAvatarListItem, TwoLineAvatarListItem, ImageLeftWidget
from kivy_garden.mapview import MapView, MapMarkerPopup

class Database():
    def __init__(self, **kwargs):
        self.db = sqlite3.connect('user.db')
        self.sql = self.db.cursor()
        print("DATABASE: Initialized users class.")

    def debug(self):
        self.sql.execute("DELETE FROM appointmentstb")
        # self.sql.execute('''CREATE TABLE appointmentstb
        #     (email text, schedule date, doctor text, reason text, addres text, stats text)''')

        # self.sql.execute("INSERT INTO userstb VALUES ('Mike','M','Myers', '095482081', '1', '1', false, 'Civil Engineer', '[0.43, 123.88]')")
        self.db.commit()

    def insertAppointment(self, email, schedule, doctor, reason, address):
        print("DATABASE: insertappointment")
        self.sql.execute("INSERT INTO appointmentstb VALUES ('{0}','{1}','{2}', '{3}', '{4}', 'pending')".format(
            email, schedule, doctor, reason, address
        ))
        self.db.commit()

    def insert(self, first, mid, last, contact, email, password, type, prof, location):
        print("DATABASE: insert")
        self.sql.execute("INSERT INTO userstb VALUES ('{0}','{1}','{2}', '{3}', '{4}', '{5}', {6}, '{7}', '{8}')".format(
            first, mid, last, contact, email, password, type, prof, location
        ))
        self.db.commit()

    def getAccountData(self, email, data):
        if data == 'password':
            self.data = self.sql.execute("SELECT pass FROM userstb WHERE email"+"="+"'{0}'".format(email)).fetchall()
            return self.data[0][0]
        elif data == 'fname':
            self.data = self.sql.execute("SELECT fname FROM userstb WHERE email"+"="+"'{0}'".format(email)).fetchall()
            return self.data[0][0]
        elif data == 'lname':
            self.data = self.sql.execute("SELECT lname FROM userstb WHERE email"+"="+"'{0}'".format(email)).fetchall()
            return self.data[0][0]
        elif data == 'profession':
            self.data = self.sql.execute("SELECT profession FROM userstb WHERE email"+"="+"'{0}'".format(email)).fetchall()
            return self.data[0][0]
        elif data == 'location':
            self.data = self.sql.execute("SELECT maploc FROM userstb WHERE email"+"="+"'{0}'".format(email)).fetchall()
            return eval(self.data[0][0])
        elif data == 'type':
            self.data = self.sql.execute("SELECT doctor FROM userstb WHERE email"+"="+"'{0}'".format(email)).fetchall()
        return self.data[0][0]

    def getDoctorBug(self, fname, lname):
        arguments = "fname='"+fname+"' AND lname='"+lname+"'"
        self.data = self.sql.execute('''SELECT email FROM userstb WHERE {0}'''.format(arguments)).fetchall()
        return self.data[0][0]       
    
    def getPostAuthor(self, post):
        self.data = self.sql.execute("SELECT email FROM poststb WHERE post"+"="+"'{0}'".format(post)).fetchall()
        print("AUTHOR IS: ", self.data[0][0])
        return self.data[0][0]

    def verifyUserExist(self, email):
        print("DATABASE: verify if user exist")
        self.data = self.sql.execute('''SELECT email FROM userstb''').fetchall()
        for x in self.data:
            if email == x[0]:
                print("DEBUG: Email exists")
                return True
        print("DEBUG: Email not exist")

    def loadBooking(self, email):
        doctor = self.getAccountData(email, 'type')
        if doctor == True:
            where = "doctor='{0}'".format(email)
            self.data = self.sql.execute("SELECT * FROM appointmentstb WHERE {0}".format(where)).fetchall()
            return self.data
        else:
            where = "email='{0}'".format(email)
            self.data = self.sql.execute("SELECT * FROM appointmentstb WHERE {0} ORDER BY schedule".format(where)).fetchall()
            return self.data

    def getDoctors(self):
        where = "doctor=1"
        self.data = self.sql.execute("SELECT email FROM userstb WHERE {0}".format(where)).fetchall()
        list_doctors = []
        for doctors in self.data:
            list_doctors.append(doctors[0])
        return list_doctors
    
    def insertPost(self, author, post):
        self.sql.execute("INSERT INTO poststb VALUES ('{}','{}')".format(author, post))
        self.db.commit()

    def deletePost(self, email, discardedpost):
        post = "post = '{0}'".format(discardedpost)
        self.sql.execute("DELETE FROM poststb WHERE {0}".format(post))
        self.db.commit()

    def updateLocation(self, email, location):
        newloc = "maploc = '{0}'".format(location)
        emailcommand = "email = '{0}'".format(email)
        self.sql.execute("UPDATE userstb SET {0} WHERE {1}".format(newloc, emailcommand))
        self.db.commit()
        print("SUCCESSFULLY UPDATED")
        # UsersDB.update({'location': location}, User.email == email)

    def getposts(self):
        posts_dict = {}
        self.data = self.sql.execute("SELECT * FROM poststb").fetchall()
        for x in self.data:
            posts_dict[x[1]] = x[0]
        return posts_dict


class LoginScreen(Screen):
    print("INITIALIZED: LOGIN SCREEN")
    
    # Login Verification
    def verifyUser(self):
        global userlogged
        if usersDB.verifyUserExist(self.ids.useremail.text) == True:
            userlogged = self.ids.useremail.text
            print("USER " + userlogged + " EXISTS")
            if self.ids.userpass.text == usersDB.getAccountData(userlogged, 'password'):
                if usersDB.getAccountData(userlogged, 'type') == True:
                    self.parent.get_screen("kv_menu").ids.doctorbutton.text = "My Location"
                else:
                    self.parent.get_screen("kv_menu").ids.doctorbutton.text = "Find Doctor"
                name = usersDB.getAccountData(userlogged, 'fname') + "  " + usersDB.getAccountData(userlogged, 'lname')
                self.parent.get_screen("kv_menu").navname.text = name
                self.ids.useremail.text = ""
                self.ids.userpass.text = ""
                self.updatePostWall()
                print("DEBUG: " + userlogged + " has logged in.")
                self.parent.current = "kv_menu"
            else:
                self.ids.loginlabel.text = "Invalid Password!"
        else:
            self.ids.loginlabel.text = "Invalid Email!"

    # Automatically insert data to MenuScreen post wall
    def updatePostWall(self):
        self.parent.get_screen("kv_menu").ids.list_on_menu.clear_widgets()
        results = usersDB.getposts()
        for post in reversed(results):
            occupation = usersDB.getAccountData(results[post], 'profession')
            firstname = usersDB.getAccountData(results[post], 'fname')
            lastname = usersDB.getAccountData(results[post], 'lname')
            primary_text = firstname + " " + lastname + " (" + occupation + ")"
            textprofile = MDRoundFlatButton(text = primary_text, size_hint = (None, 0.2))
            text = MDLabel(text = post, size_hint_y = 0.3)
            underline = MDLabel(text = "_"*54, halign = "center", size_hint_y = 0.3)
            self.parent.get_screen("kv_menu").ids.list_on_menu.add_widget(textprofile)
            self.parent.get_screen("kv_menu").ids.list_on_menu.add_widget(text)
            self.parent.get_screen("kv_menu").ids.list_on_menu.add_widget(underline)
        print("DEBUG: Successfully loaded posts to menu.")
    

class CreateAccountScreen(Screen):
    print("INITIALIZED: CREATE ACCOUNT SCREEN")

    # Button for toggling accounts type
    def toggleType(self):
        if (self.ids.toggletype.text == 'DOCTOR ACCOUNT'):
            self.ids.toggletype.text = 'STANDARD ACCOUNT'
            self.ids.profession.hint_text = "Profession"
        elif (self.ids.toggletype.text == 'STANDARD ACCOUNT'):
            self.ids.toggletype.text = 'DOCTOR ACCOUNT'
            self.ids.profession.hint_text = "Specialization"
        print("DEBUG: Toggling account type button")
    
    def createAccountDB(self):
        if self.ids.toggletype.text == 'DOCTOR ACCOUNT':
            acc_type = True
        else:
            acc_type = False
        email =  self.ids.newemail.text
        password = self.ids.newpass.text
        first = self.ids.newfirst.text
        mid = self.ids.newmiddle.text
        last = self.ids.newlast.text
        contact = self.ids.contact.text
        prof = self.ids.profession.text
        usersDB.insert(first, mid, last, contact, email, password, acc_type, prof, "[11, 121]")
        self.parent.get_screen("kv_login").ids.loginlabel.text = "Successfully Created Account!\n You can now login " + first
        self.clear()
        print("DEBUG: Successfuly created account.", email)

    
    def clear(self):
        self.ids.newemail.text = ""
        self.ids.newpass.text = ""
        self.ids.newfirst.text = ""
        self.ids.newmiddle.text = ""
        self.ids.newlast.text = ""
        self.ids.contact.text = ""
        self.ids.profession.text = ""


class MenuScreen(Screen):
    print("INITIALIZED: MENU SCREEN")

    # Automatically creates user's marker in the "set location" map screen
    def setInitialLocation(self):
        global final_location, location_marker, userlogged
        locationlist = usersDB.getAccountData(userlogged, 'location')
        location_marker = MapMarkerPopup(lat = locationlist[0], lon = locationlist[1], source = "icons/you.png")
        self.parent.get_screen("kv_locationmapview").ids.locationmapview.add_widget(location_marker)
        final_location = locationlist
        print("DEBUG: Initial location has been set.")

    def initializeBookingPage(self):
        # self.parent.get_screen("kv_listbooking").ids.bookinglist.add_widget()
        doctor = usersDB.getAccountData(userlogged, 'type')
        results = usersDB.loadBooking(userlogged)
        if doctor == True:
            for appointments in results:
                if appointments[2] == userlogged:
                    primary_text = appointments[0]
                    secondary_text = str(appointments[1])
                    tertiary_text = appointments[3]
                    profile = ThreeLineAvatarListItem(text = primary_text, secondary_text = secondary_text, tertiary_text = tertiary_text)
                    self.parent.get_screen("kv_listbooking").ids.bookinglist.add_widget(profile)
                    print("DEBUG: Added a appointment in doctor's list")
                else:
                    pass
        else:
            for appointments in results:
                if appointments[0] == userlogged:
                    primary_text = appointments[2]
                    secondary_text = str(appointments[1])
                    tertiary_text = appointments[5]
                    profile = ThreeLineAvatarListItem(text = primary_text, secondary_text = secondary_text, tertiary_text = tertiary_text)
                    self.parent.get_screen("kv_listbooking").ids.bookinglist.add_widget(profile)
                    print("DEBUG: Added a appointment to user's pending list")
                else:
                    pass
        

    def loggingout(self):
        self.parent.get_screen("kv_login").ids.loginlabel.text = "You have been logged out.\n Thanks for using MedCheck " + usersDB.getAccountData(userlogged, 'fname')

    def clearposts(self):
        self.parent.get_screen("kv_menu").ids.list_on_menu.clear_widgets()


class DeletePostScreen(Screen):
    dialog = None

    def buttonPress(self):
        if (self.ids.buttondelete.text == 'LOAD MY POSTS'):
            print("lod post")
            self.ids.buttondelete.text = "Back"
            self.ids.delete_label.text = "Your posts have been loaded"
            self.deletePost()
        elif (self.ids.buttondelete.text == "Back"):
            self.ids.delete_list.clear_widgets()
            self.ids.buttondelete.text = 'LOAD MY POSTS'
            self.ids.delete_label.text = "Any deletions of posts cannot be undone"
            self.parent.current = "kv_menu"



    # Function to load the user's posts
    def deletePost(self):
        results = usersDB.getposts()
        users_results = []
        for post in reversed(results):
            if usersDB.getPostAuthor(post) == userlogged:
                users_results.append(post)
        for user_post in reversed(users_results):
            secondary_text = user_post
            textprofile = MDRoundFlatButton(text = "REMOVE", size_hint = (None, 0.2), on_release = lambda x:self.deletenow(user_post))
            text = MDLabel(text = secondary_text, size_hint_y = 0.3)
            underline = MDLabel(text = "_"*54, halign = "center", size_hint_y = 0.3)
            self.ids.delete_list.add_widget(textprofile)
            self.ids.delete_list.add_widget(text)
            self.ids.delete_list.add_widget(underline)
        print("DEBUG: Successfully Loaded DELETE posts to menu.")

    # Popup function to confirm the deletion of post 
    def deletenow(self, postdialogue):
        if not self.dialog:
            self.dialog = MDDialog(
            text="Discard Post?\n"+postdialogue,
            size_hint = (None, None),
            size = (200, 300),
            buttons=[MDRoundFlatButton(text="CANCEL", on_release = lambda x:self.dialog.dismiss()),MDRoundFlatButton(text="DISCARD", on_release = lambda x:self.deletedscreen(postdialogue)),],
            )
        self.dialog.open()

     
    def deletedscreen(self, post):
        self.ids.delete_label.text = "({0}) has been deleted".format(post)
        self.dialog.dismiss()
        usersDB.deletePost(userlogged, post)
        self.ids.delete_list.clear_widgets()
        results = usersDB.getposts()
        for post in reversed(results):
            secondary_text = post
            if userlogged == results[post]:
                textprofile = MDRoundFlatButton(text = "REMOVE YOUR POST", size_hint = (None, 0.2), on_release = lambda x:self.deletenow(post))
                text = MDLabel(text = secondary_text, size_hint_y = 0.3)
                underline = MDLabel(text = "_"*54, halign = "center", size_hint_y = 0.3)
                self.ids.delete_list.add_widget(textprofile)
                self.ids.delete_list.add_widget(text)
                self.ids.delete_list.add_widget(underline)
        print("DEBUG: Successfully deleted, refreshing list")


class NewPostScreen(Screen):
    dialog = None

    # Function to append new post and refresh list
    def appendPost(self):
        newpost = self.ids.postbox.text
        usersDB.insertPost(userlogged, newpost)
        self.parent.get_screen("kv_menu").ids.list_on_menu.clear_widgets()
        global postwallwidgets
        postwallwidgets = []
        results = usersDB.getposts()
        for post in reversed(results):
            occupation = usersDB.getAccountData(results[post], 'profession')
            firstname = usersDB.getAccountData(results[post], 'fname')
            lastname = usersDB.getAccountData(results[post], 'lname')
            primary_text = firstname + " " + lastname + " (" + occupation + ")"
            secondary_text = post
            textprofile = MDRoundFlatButton(text = primary_text, size_hint = (None, 0.2))
            text = MDLabel(text = secondary_text, size_hint_y = 0.3)
            underline = MDLabel(text = "_"*54, halign = "center", size_hint_y = 0.3)
            self.parent.get_screen("kv_menu").ids.list_on_menu.add_widget(textprofile)
            self.parent.get_screen("kv_menu").ids.list_on_menu.add_widget(text)
            self.parent.get_screen("kv_menu").ids.list_on_menu.add_widget(underline)
        print("DEBUG: Successfully loaded posts to menu.")

    def clear(self):
        self.ids.postbox.text = ""


class ProfileScreen(Screen):
    print("INITIALIZED: PROFILE SCREEN")
    pass


class LocationMapViewScreen(Screen):
    print("INITIALIZED: LOCATION MAP VIEW SCREEN")

    # Button function to set new marker
    def setMarker(self):
        global location_marker, final_location
        latitude = self.ids.locationmapview.lat
        longitude = self.ids.locationmapview.lon

        if self.ids.locationsetlabel.text == 'Your Location':
            self.ids.locationmapview.remove_marker(location_marker)
            location_marker = MapMarkerPopup(lat = latitude, lon = longitude, source = "icons/you.png")
            self.ids.locationmapview.add_widget(location_marker) 
            self.ids.locationsetlabel.text = 'Location Updated!'
            final_location = "[" + str(latitude) + ", " + str(longitude) + "]"
        elif self.ids.locationsetlabel.text == 'Location Updated!':
            self.ids.locationmapview.remove_marker(location_marker) 
            location_marker = MapMarkerPopup(lat = latitude, lon = longitude, source = "icons/you.png")
            self.ids.locationmapview.add_widget(location_marker)
            final_location = "[" + str(latitude) + ", " + str(longitude) + "]"
        print("DEBUG: New location marker has been set.")

    # Automatically saves new user location to database
    def updateLocation(self):
        global final_location, location_marker
        usersDB.updateLocation(userlogged, final_location)
        self.ids.locationmapview.remove_marker(location_marker) 
        print("DEBUG: User location has been updated. ", final_location)
        self.ids.locationsetlabel.text = 'Your Location'
        if usersDB.getAccountData(userlogged, 'type') == True:
            self.parent.current = "kv_menu"
        else:
            self.loadDoctors()
            self.parent.current = "kv_doctorlistview"

    # Loads all doctors in Map/List view screen
    def loadDoctors(self):

        # Creates a delete list for marker/list widgets
        global delete_list
        delete_list = []

        # Loads all doctors and calculate their distance through Harverstine formula
        results = usersDB.getDoctors()
        list_of_doctors = {}
        for doctor in results:
            location = usersDB.getAccountData(doctor, 'location')
            list_of_doctors[doctor] = location
        sorted_list = self.calculateHaversine(list_of_doctors)
        print("DEBUG: List has been sorted.\n", sorted_list)

        # Appends the sorted doctor list to the list view screen
        for doctors in sorted_list:
            distance = ""
            doctor_email = doctors[0]
            if (doctors[1] > 999):
                distance = str(round((doctors[1] / 1000), 1)) + "K KM"
            elif (doctors[1] <= 999):
                distance = (str(doctors[1]) + " KM")
            primary_text = usersDB.getAccountData(doctor_email, 'fname') + " " + usersDB.getAccountData(doctor_email, 'lname')
            secondary_text = usersDB.getAccountData(doctor_email, 'profession')
            profile = ThreeLineAvatarListItem(text = primary_text, secondary_text = secondary_text, tertiary_text = distance, on_release = lambda doctor_email:self.loadDoctorBooking(doctor_email))
            exist = True
            try:
                image = open("profiles/"+doctor_email+".jpg")
            except IOError:
                exist = False
            if exist == True:
                picture = ImageLeftWidget(source = "profiles/"+doctor_email+".jpg")
            else:
                picture = ImageLeftWidget(source = "profiles/default.png")
            profile.add_widget(picture)
            self.parent.get_screen("kv_doctorlistview").ids.doctor_list.add_widget(profile)
            print("DEBUG: Added a doctor to list")

        # Creates a marker for the user's location in map view screen, appends to delete list for later
        user_location = usersDB.getAccountData(userlogged, 'location')
        user_marker = MapMarkerPopup(lat = user_location[0], lon = user_location[1], source = "icons/you.png")
        self.parent.get_screen("kv_doctormapview").ids.automaticmapview.add_widget(user_marker)
        delete_list.append(user_marker)

        # Creates map marker for all doctors in map view screen, appends to the delete list for later
        for doctor in results:
            location = usersDB.getAccountData(doctor, 'location')
            marker = MapMarkerPopup(lat = location[0], lon = location[1], source = 'icons/marker.png')
            existinMap = True
            try:
                imagemap = open("profiles/"+doctor_email+".jpg")
            except IOError:
                existinMap = False
            if existinMap == True:
                marker.add_widget(Button(background_normal = "profiles/" + doctor + ".jpg"))
            else:
                marker.add_widget(Button(background_normal = "profiles/default.png"))
            self.parent.get_screen("kv_doctormapview").ids.automaticmapview.add_widget(marker) 
            delete_list.append(marker)
            print("DEBUG: Added a doctor to map")
        print("DEBUG: Successfully loaded doctors to list/map view.")

    # Haversine's Algorithm, returns the sorted distances of the doctors
    def calculateHaversine(self, list_doctors):
        raw_list = list_doctors
        user_location = usersDB.getAccountData(userlogged, 'location')

        # Apply the formula to each location of the doctors
        for location in raw_list:
            doctor_location = raw_list[location]
            lat1 = user_location[0] 
            lon1 = user_location[1]
            lat2 = doctor_location[0]
            lon2 = doctor_location[1]
            radius = 6371  # kilo meter conversion
            dlat = math.radians(lat2-lat1)
            dlon = math.radians(lon2-lon1)
            a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
                * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            distance = radius * c
            raw_list.pop(location)
            raw_list[location] = int(distance)
        print("DEBUG: List has been updated.\n", raw_list)
        return sorted(raw_list.items(), key = lambda x: x[1])

    # Load doctor in list to booking screen
    def loadDoctorBooking(self, doctor):
        global sm
        sm.get_screen("kv_bookpatient").ids.doctorlabel.text = doctor.text
        sm.current = "kv_bookpatient"
            
            
class DoctorListViewScreen(Screen):
    print("INITIALIZED: FIND AUTOMATIC SCREEN")

    # Deletes all widgets in the delete list, before moving back to previous screen
    def resetWidgets(self):
        global delete_list
        for marker in delete_list:
            self.parent.get_screen("kv_doctormapview").ids.automaticmapview.remove_marker(marker) 
        self.ids.doctor_list.clear_widgets()


class DoctorMapViewScreen(Screen):
    print("INITIALIZED: AUTOMATIC MAP VIEW SCREEN")
    def delete_widgets(self):
        pass


class PatientBookingScreen(Screen):
    print("INITIALIZED: PATIENT BOOKING SCREEN")
    dialog = None
    date = None

    def submitForm(self):
        if not self.dialog:
            self.dialog = MDDialog(
            text="Submit Booking\n{0}\n{1}\n{2}".format(self.ids.doctorlabel.text, self.date, self.ids.bookreason.text),
            size_hint = (None, None),
            size = (200, 300),
            buttons=[MDRoundFlatButton(text="BACK", on_release = lambda x:self.dismiss()),MDRoundFlatButton(text="CONFIRM", on_release = lambda x:self.patientBookingDB(self.date)),],
            )
        self.dialog.open()

    def show_datepicker(self):
        picker = MDDatePicker(callback = self.got_date)
        picker.open()
    
    def got_date(self, the_date):
        self.date = the_date
    
    def dismiss(self):
        self.dialog.dismiss()
        self.date = None
        self.dialog = None

    def patientBookingDB(self, date):
        global sm
        self.dismiss()
        doctorname = self.ids.doctorlabel.text.split()
        email = usersDB.getDoctorBug(doctorname[0], doctorname[1])
        usersDB.insertAppointment(userlogged, date, email, self.ids.bookreason.text, self.ids.address1.text)
        self.ids.bookreason.text = ""
        self.ids.address1.text = ""
        print("SUCCESSFULLY BOOKED PATIENT TO DATABASE")
        sm.current = "kv_doctorlistview"

    def backbutton(self):
        self.ids.bookreason.text = ""
        self.ids.address1.text = ""


class ListBookingScreen(Screen):
    print("INITIALIZED: BOOKING LIST VIEW SCREEN")

    def clear(self):
        self.ids.bookinglist.clear_widgets()

# Main build class
class medcheckApp(MDApp):
    def build(self):
        global sm
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name = 'kv_login'))
        sm.add_widget(CreateAccountScreen(name = 'kv_createaccount'))
        sm.add_widget(MenuScreen(name = 'kv_menu'))
        sm.add_widget(ProfileScreen(name = 'kv_profile'))
        sm.add_widget(DoctorListViewScreen(name = 'kv_doctorlistview'))
        sm.add_widget(DoctorMapViewScreen(name = 'kv_doctormapview'))
        sm.add_widget(LocationMapViewScreen(name = 'kv_locationmapview'))
        sm.add_widget(NewPostScreen(name = 'kv_newpostscreen'))
        sm.add_widget(DeletePostScreen(name = 'kv_deletepostscreen'))
        sm.add_widget(PatientBookingScreen(name='kv_bookpatient'))
        sm.add_widget(ListBookingScreen(name='kv_listbooking'))
        print("INITIALIZED: SCREEN MANAGER AND SCREENS")
        return sm


if __name__ == "__main__":
    # Database Initialization
    usersDB = Database()
    userlogged = ""

    # usersDB.debug()
    # print("OK")

    # # Kivy Initialization
    Window.size = (390, 700)

    print("INITIALIZED: MAIN")
    medcheckApp().run()


