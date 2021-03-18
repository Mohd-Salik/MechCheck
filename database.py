from tinydb import TinyDB, Query

# Database class
class Database():
    def __init__(self, **kwargs):
        print("INITIALIZED: DataBase")

    def insert(self, first, mid, last, contact, email, password, type, prof, location):
        print("CALLED: insert")
        db.insert({'firstname': first, 'middlename': mid, 'lastname': last, 'contact': contact, 'email': email, 'password': password, 'type': type, 'profession': prof, 'location': location})

    def searchUser(self, email):
        print("CALLED: searchUser")
        results = db.search(User.email == email)
        return results

    def findDoctors(self):
        print("CALLED: findDoctors")
        results = db.search(User.type == 'doctor')
        return results

db = TinyDB('db.json')
User = Query()