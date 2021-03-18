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


class MenuScreen(Screen):
    print("INITIALIZED: MENU SCREEN")
    usernameText = StringProperty('username label')


class ProfileScreen(Screen):
    print("INITIALIZED: PROFILE SCREEN")
    pass


class LoginScreen(Screen):
    print("INITIALIZED: LOGIN SCREEN")
    def initializeUser(self):
        print("CALLED: initializeUser")
        userlogged = data.searchUser(self.userlogged.text)   
        username = (userlogged[0]['firstname'] + " " + userlogged[0]['lastname'])
        self.manager.get_screen('kv_menu').usernameText = username


class FindDoctorScreen(Screen):
    print("INITIALIZED: FIND DOCTOR SCREEN")

class FindAutomaticScreen(Screen):
    print("INITIALIZED: FIND AUTOMATIC SCREEN")
    def addAutomaticDoctorsList(self):
        print("CALLED: addAutomaticDoctorsList")
        self.ids.doctor_list.clear_widgets()
        results = data.findDoctors()
        for doctor in results:
            profile = ThreeLineAvatarListItem(text = doctor['firstname'] + " " + doctor ['lastname'], secondary_text = doctor['profession'], tertiary_text = doctor['contact'])
            picture = ImageLeftWidget(source = 'profiles/'+ doctor['email'] + '.jpg')
            profile.add_widget(picture)
            self.ids.doctor_list.add_widget(profile)
            print("ADDED: doctor to list")


class AutomaticMapViewScreen(Screen):
    print("INITIALIZED: AUTOMATIC MAP VIEW SCREEN")
    def addMapAutomaticDoctorsList(self):
        print("CALLED: addMapAutomaticDoctorsList")
        results = data.findDoctors()
        for doctor in results:
            location = eval(doctor['location'])
            marker = MapMarkerPopup(lat = location[0], lon = location[1], source = 'profiles/marker.png')
            marker.add_widget(Button(background_normal = "profiles/" + doctor['email'] + ".jpg"))
            self.ids.automaticmapview.add_widget(marker) 
            print("ADDED: marker to map")     


class LocationMapViewScreen(Screen):
    print("INITIALIZED: LOCATION MAP VIEW SCREEN")



# Main build class
class medcheckApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name = 'kv_login'))
        sm.add_widget(MenuScreen(name = 'kv_menu'))
        sm.add_widget(ProfileScreen(name = 'kv_profile'))
        sm.add_widget(FindDoctorScreen(name = 'kv_finddoctor'))
        sm.add_widget(FindAutomaticScreen(name = 'kv_findautomatic'))
        sm.add_widget(AutomaticMapViewScreen(name = 'kv_automaticmapview'))
        sm.add_widget(LocationMapViewScreen(name = 'kv_locationmapview'))

        print("INITIALIZED: SCREEN MANAGER AND SCREENS")
        return sm

if __name__ == "__main__":
    # Database Initialization
    data = Database()
    userlogged = []

    # Kivy Initialization
    userlogged = []
    Window.size = (390, 700)

    print("INITIALIZED: MAIN")

    medcheckApp().run()


