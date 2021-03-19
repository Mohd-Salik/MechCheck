from tinydb import TinyDB, Query

# Database class
class Database():
    def __init__(self, **kwargs):
        print("DATABASE: Initialized class.")

    def insert(self, first, mid, last, contact, email, password, type, prof, location):
        print("DATABASE: insert")
        db.insert({'firstname': first, 'middlename': mid, 'lastname': last, 'contact': contact, 'email': email, 'password': password, 'type': type, 'profession': prof, 'location': location})

    def getAccountData(self, email, data):
        results = db.search(User.email == email)
        print("DATABASE: Return ", data, " of: ", email)
        return results[0][data]
        # if (data == "first_name"):
        #     return results['firstname'] 
        # elif (data == "middle_name"):
        #     return results['middlename'] 
        # elif (data == "last_name"):
        #     return results['lastname'] 
        # elif (data == "contact"):
        #     return results['contact'] 
        # elif (data == "email"):
        #     return results['email'] 
        # elif (data == "password"):
        #     return results['password'] 
        # elif (data == "type"):
        #     return results['type'] 
        # elif (data == "profession"):
        #     return results['profession'] 
        # elif (data == "location"):
        #     return results['location'] 

    def verifyUserExist(self, email):
        print("DATABASE: verify if user exist")
        
        if len(db.search(User.email == email)) > 0:
            return True
        else:
            return False

    def getDoctors(self):
        print("DATABASE: find all Doctors")
        results = db.search(User.type == 'doctor')
        return results

    def updateLocation(self, email, location):
        db.update({'location': location}, User.email == email)

db = TinyDB('db.json')
User = Query()