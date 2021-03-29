from tinydb import TinyDB, Query

# Database class
class UsersClass():
    def __init__(self, **kwargs):
        print("DATABASE: Initialized users class.")

    def insert(self, first, mid, last, contact, email, password, type, prof, location):
        print("DATABASE: insert")
        UsersDB.insert({'firstname': first, 'middlename': mid, 'lastname': last, 'contact': contact, 'email': email, 'password': password, 'type': type, 'profession': prof, 'location': location})

    def getAccountData(self, email, data):
        results = UsersDB.search(User.email == email)
        print("DATABASE: Return ", data, " of: ", email)
        return results[0][data]

    def verifyUserExist(self, email):
        print("DATABASE: verify if user exist")
        
        if len(UsersDB.search(User.email == email)) > 0:
            return True
        else:
            return False

    def getDoctors(self):
        print("DATABASE: find all Doctors")
        results = UsersDB.search(User.type == 'doctor')
        return results

    def updateLocation(self, email, location):
        UsersDB.update({'location': location}, User.email == email)

class PostsClass():
    def __init__(self, **kwargs):
        print("DATABASE: Initialized posts class.")

    def getposts(self):
        return PostsDB.all()
        

UsersDB = TinyDB('UsersDB.json')
PostsDB = TinyDB('PostsDB.json')
User = Query()


