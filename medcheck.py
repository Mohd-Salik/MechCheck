import math
from collections import OrderedDict
from database import Database

from kivymd.app import MDApp
from kivymd.uix.button import Button
from kivymd.uix.screen import Screen
from kivy_garden.mapview import MapView
from kivy_garden.mapview import MapMarkerPopup
from kivymd.uix.list import OneLineAvatarListItem
from kivymd.uix.list import ThreeLineAvatarListItem,ImageLeftWidget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty


class LoginScreen(Screen):
    print("INITIALIZED: LOGIN SCREEN")
    
    def verifyUser(self):
        global userlogged
        if data.verifyUserExist(self.useremail.text) == True:
            userlogged = self.useremail.text
            print("USER " + userlogged + " EXISTS")
            if self.userpass.text == data.getAccountData(userlogged, 'password'):
                self.parent.get_screen("kv_menu").usernameText = name
                name = data.getAccountData(userlogged, 'firstname') + data.getAccountData(userlogged, 'lastname')
                print("DEBUG: " + userlogged + " has logged in.")
                
                self.parent.current = "kv_menu"
            else:
                self.ids.loginlabel.text = "wrong password"
        else:
            self.ids.loginlabel.text = "username does not exist"


class CreateAccountScreen(Screen):
    print("INITIALIZED: CREATE ACCOUNT SCREEN")

    # Button for toggling accounts type
    def toggleType(self):
        if (self.ids.toggletype.text == 'DOCTOR ACCOUNT'):
            self.ids.toggletype.text = 'STANDARD ACCOUNT'
        elif (self.ids.toggletype.text == 'STANDARD ACCOUNT'):
            self.ids.toggletype.text = 'DOCTOR ACCOUNT'
        print("DEBUG: Toggling account type button")
    
    def createAccountDB(self):
        acc_type =  self.ids.toggletype.text
        email =  self.ids.newemail.text
        password = self.ids.newpass.text
        first = self.ids.newfirst.text
        mid = self.ids.newmiddle.text
        last = self.ids.newlast.text
        contact = self.ids.contact.text
        prof = self.ids.profession.text
        data.insert(first, mid, last, contact, email, password, acc_type, prof, "[11, 121]")
        print("DEBUG: Successfuly created account.")


class MenuScreen(Screen):
    print("INITIALIZED: MENU SCREEN")
    usernameText = StringProperty('username label')


class ProfileScreen(Screen):
    print("INITIALIZED: PROFILE SCREEN")
    pass


class FindDoctorScreen(Screen):
    print("INITIALIZED: FIND DOCTOR SCREEN")

    # Automatically creates user's marker in the "set location" map screen
    def setInitialLocation(self):
        global final_location, location_marker, userlogged
        locationlist = data.getAccountData(userlogged, 'location')
        location_marker = MapMarkerPopup(lat = eval(locationlist)[0], lon = eval(locationlist)[1], source = "profiles/you.png")
        self.parent.get_screen("kv_locationmapview").ids.locationmapview.add_widget(location_marker)
        final_location = locationlist
        print("DEBUG: Initial location has been set.")


class LocationMapViewScreen(Screen):
    print("INITIALIZED: LOCATION MAP VIEW SCREEN")

    # Button function to set new marker
    def setMarker(self):
        global location_marker, final_location
        latitude = self.ids.locationmapview.lat
        longitude = self.ids.locationmapview.lon

        if self.ids.locationsetlabel.text == 'Set Location':
            self.ids.locationmapview.remove_marker(location_marker)
            location_marker = MapMarkerPopup(lat = latitude, lon = longitude, source = "profiles/you.png")
            self.ids.locationmapview.add_widget(location_marker) 
            self.ids.locationsetlabel.text = 'Click Next'
            final_location = "[" + str(latitude) + ", " + str(longitude) + "]"
        elif self.ids.locationsetlabel.text == 'Click Next':
            self.ids.locationmapview.remove_marker(location_marker) 
            location_marker = MapMarkerPopup(lat = latitude, lon = longitude, source = "profiles/you.png")
            self.ids.locationmapview.add_widget(location_marker)
            final_location = "[" + str(latitude) + ", " + str(longitude) + "]"
        print("DEBUG: New location marker has been set.")

    # Automatically saves new user location to database
    def updateLocation(self):
        global final_location, location_marker
        data.updateLocation(userlogged, final_location)
        self.ids.locationmapview.remove_marker(location_marker) 
        print("DEBUG: User location has been updated. ", final_location)

    # Loads all doctors in Map/List view screen
    def loadDoctors(self):

        # Creates a delete list for marker/list widgets
        global delete_list
        delete_list = []

        # Loads all doctors and calculate their distance through Harverstine formula
        results = data.getDoctors()
        list_of_doctors = {}
        for doctor in results:
            list_of_doctors[doctor['location']] = doctor['email']
        sorted_list = self.calculateHaversine(list_of_doctors)
        print("DEBUG: List has been sorted.\n", sorted_list)

        # Appends the sorted doctor list to the list view screen
        for doctors in sorted_list:
            distance = ""
            doctor_email = doctors[1]
            if (doctors[0] > 999):
                distance = str(round((doctors[0] / 1000), 1)) + "K KM"
            elif (doctors[0] <= 999):
                distance = (str(doctors[0]) + " KM")
            primary_text = data.getAccountData(doctor_email, 'firstname') + " " + data.getAccountData(doctor_email, 'lastname')
            secondary_text = data.getAccountData(doctor_email, 'firstname')
            profile = ThreeLineAvatarListItem(text = primary_text, secondary_text = secondary_text, tertiary_text = distance)
            picture = ImageLeftWidget(source = 'profiles/'+ doctor_email + '.jpg')
            profile.add_widget(picture)
            self.parent.get_screen("kv_doctorlistview").ids.doctor_list.add_widget(profile)
            print("DEBUG: Added a doctor to list")

        # Creates a marker for the user's location in map view screen, appends to delete list for later
        user_location = eval(data.getAccountData(userlogged, 'location'))
        user_marker = MapMarkerPopup(lat = user_location[0], lon = user_location[1], source = "profiles/you.png")
        self.parent.get_screen("kv_doctormapview").ids.automaticmapview.add_widget(user_marker)
        delete_list.append(user_marker)

        # Creates map marker for all doctors in map view screen, appends to the delete list for later
        for doctor in results:
            location = eval(doctor['location'])
            marker = MapMarkerPopup(lat = location[0], lon = location[1], source = 'profiles/marker.png')
            marker.add_widget(Button(background_normal = "profiles/" + doctor['email'] + ".jpg"))
            self.parent.get_screen("kv_doctormapview").ids.automaticmapview.add_widget(marker) 
            delete_list.append(marker)
            print("DEBUG: Added a doctor to map")
        print("DEBUG: Successfully loaded doctors to list/map view.")

    # Haversine's Algorithm, returns the sorted distances of the doctors
    def calculateHaversine(self, list_doctors):
        raw_list = list_doctors
        user_location = eval(data.getAccountData(userlogged, 'location'))

        # Apply the formula to each location of the doctors
        for location in raw_list:
            doctor_location = eval(location)
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
            raw_list[int(distance)] = raw_list.pop(location)
        print("DEBUG: List has been updated.\n", raw_list)

        return sorted(raw_list.items(), key = lambda x: x[1])
            
            
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


# Main build class
class medcheckApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name = 'kv_login'))
        sm.add_widget(CreateAccountScreen(name = 'kv_createaccount'))
        sm.add_widget(MenuScreen(name = 'kv_menu'))
        sm.add_widget(ProfileScreen(name = 'kv_profile'))
        sm.add_widget(FindDoctorScreen(name = 'kv_finddoctor'))
        sm.add_widget(DoctorListViewScreen(name = 'kv_doctorlistview'))
        sm.add_widget(DoctorMapViewScreen(name = 'kv_doctormapview'))
        sm.add_widget(LocationMapViewScreen(name = 'kv_locationmapview'))
        print("INITIALIZED: SCREEN MANAGER AND SCREENS")
        return sm


if __name__ == "__main__":
    # Database Initialization
    data = Database()

    # Kivy Initialization
    userlogged = ""
    Window.size = (390, 700)

    print("INITIALIZED: MAIN")
    medcheckApp().run()


