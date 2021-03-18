from tinydb import TinyDB, Query

# Database class
class Database():
    def __init__(self, **kwargs):
        print("INITIALIZED: DataBase")

    def insert(self, first, mid, last, contact, email, password, type, prof, location):
        print("CALLED: insert")
        db.insert({'firstname': first, 'middlename': mid, 'lastname': last, 'contact': contact, 'email': email, 'password': password, 'type': type, 'profession': prof, 'location': location})


    def verifyUserExist(self, email):
        print("CALLED: verify if user exist")
        results = db.search(User.email == email)
        if len(results) > 0:
            return True
        else:
            return False

    def searchUser(self, email):
        print("CALLED: searchUser: " + email)
        results = db.search(User.email == email)
        return results

    def findDoctors(self):
        print("CALLED: find all Doctors")
        results = db.search(User.type == 'doctor')
        return results

db = TinyDB('db.json')
User = Query()

# db.remove(User.firstname == 'asd')