import csv
#import pyminizip
import pandas as pd
from os.path import exists

class CSVHandler():

    def __init__(self, filename_credentials='users.csv', filename_results='results.csv'):
        super().__init__()

        self.patientLists={}

        # Default file names
        self.filename_credentials = filename_credentials
        #open(self.filename_credentials, 'a+', newline='')
        self.writer_credentials = None
        self.reader_credentials = None

        self.filename_results = filename_results
        #open(self.filename_results, 'a+', newline='')
        self.writer_results = None
        self.reader_results = None

        #self.credential_fieldnames = ['username', 'password']
        self.user_fieldnames = ['first_name', 'last_name', 'date_of_birth', 'organization', 'username', 'password', 'role','department','clinician name','vip','sas','tb','maze','facial expression','eyetracking']

    def create_credentials_file(self, fieldnames=None):
        if fieldnames is None:
            fieldnames = ['first_name', 'last_name', 'date_of_birth', 'organization', 'username', 'password','role','clinician name','department','vip','sas','tb','maze','facial expression','eyetracking']
            # fieldnames = ['username', 'password']

        #file_exists = exists(self.filename_credentials)
        #if not file_exists:
        empty = self.is_empty()
        if empty == 2:
            # Create a writer to the file
            self.writer_credentials = csv.DictWriter('users.csv', fieldnames=fieldnames)
            self.writer_credentials.writeheader()
            self.user_fieldnames = fieldnames
        else:
            print("credentials file already exists...")

    def create_results_file(self, fieldnames=None):
        #with open(self.filename_results, 'r +', newline='') as file_results:

        if fieldnames is None:
            fieldnames = ['time']
        self.writer_results = csv.DictWriter(self.file_results, fieldnames=fieldnames)
        self.writer_results.writeheader()
        self.reader_results = csv.reader(self.file_results)

    """
    Returns 0 if contains data
            1 if headers included but no data
            2 if completely empty
    """
    def is_empty(self):
        with open(self.filename_credentials, "r", newline='') as file_credentials:
            # skip first line of headers
            file_credentials.seek(0)
            line = file_credentials.readline()
            if line == '':
                print("file is completely empty")
                file_credentials.close()
                return 2
            #line = file_credentials.readline() #checks the second line and it would be empty even if one user is added
            if line == '':
                print("file has no data")
                return 1
            else:
                return 0

    def add_credentials(self, data=None):
        with open(self.filename_credentials, "a+", newline='') as file_credentials:
            # Create a writer to the file
            writer = csv.DictWriter(file_credentials, fieldnames=['first_name', 'last_name', 'date_of_birth', 'organization', 'username', 'password', 'role','clinician name','department','vip','sas','tb','maze','facial expression','eyetracking'])

            if self.is_empty():
                #add a check if the input data is empty maybe?
                writer.writeheader()
                writer.writerow({'first_name': data[0]["first_name"], 'last_name': data[0]["last_name"],
                                 'date_of_birth': data[0]["date_of_birth"], 'organization': data[0]["organization"],
                                 'username': data[0]["username"], 'password': data[0]['password'], 'role': data[0]['role'],'department':'N/A','clinician name':'N/A',
                                 'vip': 'False', 'sas': 'False', 'tb': 'False', 'maze': 'False','facial expression': 'False','eyetracking': 'False'})
                file_credentials.close()
                return True

            # check if user exists -> if no, add
            # Create a reader to check if user
            file_credentials.seek(0)
            reader = csv.DictReader(file_credentials)
            exists = False
            success = False
            #x = data["username"]
            #if x in reader:
            #print("bitch we made it")
            for user in data:
                for row in reader:
                    #self.reader_credentials[user["username"]] = user["password"]

                    if row["username"] == user["username"]:
                        print("User already exists.")
                        exists = True

                        break
                if not exists:
                    print(user["username"] + " added.")
                    file_credentials.seek(0)
                    writer = csv.DictWriter(file_credentials,
                                            fieldnames=['first_name', 'last_name', 'date_of_birth', 'organization',
                                                        'username', 'password', 'role', 'clinician name', 'department',
                                                        'vip', 'sas', 'tb', 'maze', 'facial expression', 'eyetracking'])
                    writer.writerow({'first_name': user["first_name"], 'last_name': user["last_name"],
                                     'date_of_birth': user["date_of_birth"], 'organization': user["organization"],
                                     'username': user["username"], 'password': user['password'], 'role': user['role'],
                                     'department': 'N/A', 'clinician name': 'N/A',
                                     'vip': 'False', 'sas': 'False', 'tb': 'False', 'maze': 'False',
                                     'facial expression': 'False', 'eyetracking': 'False'})  # changed to string false
                    success = True
            file_credentials.close()
            return success

            # self.writer_credentials.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
            # self.writer_credentials.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
            # self.writer_credentials.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

    def updatePatientDict(self):
        with open(self.filename_credentials, "a+", newline='') as file_credentials:
            file_credentials.seek(0)
            reader = csv.DictReader(file_credentials)
            for row in reader:
                self.patientLists[row["username"]]={'first_name': row["first_name"],'last_name': row["last_name"],
                                                    'date_of_birth': row["date_of_birth"], 'organization': row["organization"],
                                                    'username': row["username"],'password': row["password"],
                                                    'role': row["role"],'clinician name':row['clinician name'],'department':row['department'], 'vip': row['vip'],'sas': row['sas'],
                                                    'tb': row['tb'],'maze': row['maze'],'facial expression': row['facial expression'],'eyetracking': row['eyetracking']}
                #change the .csv file to change bool


                #self.patientLists[row["username"]]=row
        print(self.patientLists)
        file_credentials.close()
        return 1


    # test=what type of test value=True or False
    # Prototype to change csv file for test status for each patient(panda not installled so i cant use it)
    def updatePatientTestStatus(self,test,value,username):
        df=pd.read_csv("users.csv")
        df.loc[df['username']==username,test]=value
        df.to_csv('users.csv', index=False)
        df.to_csv('users.csv', index=False)
        print(df)

    """
        Returns 0 - successful login
                1 - incorrect password
               -1 - user not found   
    """
    def check_credentials(self, user=None, pw=None, org=None):
        with open(self.filename_credentials, "a+", newline='') as file_credentials:
            authorized = -1
            found = False
            # Create a reader to the file
            #with open(self.filename_credentials, 'r', newline='') as file_credentials:
            file_credentials.seek(0)
            reader = csv.DictReader(file_credentials)
            for row in reader:
                if row["username"] == user:
                    found = True
                    if row["password"] == pw and row["organization"]==org:
                        print("Login Successful")
                        authorized = 0
                        break
                    else:
                        print("Wrong Password or organization")
                        authorized = 1
                        break
            if not found:
                print("User not found")
        file_credentials.close()
        return authorized

    def get_attribute(self, person = None, attribute = 'first_name'):
        if person is None:
            return False
        with open(self.filename_credentials, "r", newline='') as file_credentials:
            file_credentials.seek(0)
            # Create a reader to the file
            reader = csv.DictReader(file_credentials)
            for row in reader:
                if row["username"] == person:
                    file_credentials.close()
                    return row[attribute]
            print("User not found")
            file_credentials.close()
            return False

    #def get_users(self):

    def windows_password_protect(self, file_name): #File name needs to passed as "./Test.csv"
        iput = file_name
        pre = None
        outp = "./output.zip"
        password = "DownToClown"
        com_lvl = 5
        pyminizip.compress(iput, None, outp, password, com_lvl)

handler = CSVHandler()
#  handler.create_credentials_file()
#  handler.add_credentials(data)
#
# data = {'first_name': 'Bitch', 'last_name': 'Boy', 'date_of_birth': 'idk', 'organization': 'hehe'},
# handler.writeCredentials(data)


"""
data = [
    {'username': 'bsantana', 'password': 'yourmom'}
    {'username': 'wrong', 'password': 'kjfdvndkjanvkj'}
]
#handler.create_credentials_file(['username', 'password'])
handler.add_credentials(data)
handler.check_credentials('bsantana', 'yourmom')
handler.check_credentials('wrong', 'oof')
data = [
    {'username': 'wrong', 'password': 'oof'}
]
handler.add_credentials(data)
handler.check_credentials('wrong', 'oof')
"""

# # prototype
# handler.create_credentials_file()
# # log in
# auth = handler.check_credentials('brolly', 'yes')
# # checks for invalid credentials
# if auth:
#     print("authorized")
# else:
#     print("not authorized")
# # adds user
# data = [
#     {'first_name': 'Braulio', 'last_name': 'Santana', 'date_of_birth': '09/01/1995', 'organization': 'RIT', 'username': 'bsantana', 'password': 'We\'re', 'role': 'patient'},
#     {'first_name': 'Maahin', 'last_name': 'Haque', 'date_of_birth': '08/17/1999', 'organization': 'RIT', 'username': 'mhaque', 'password': 'all', 'role': 'patient'},
#     {'first_name': 'Darren', 'last_name': 'De Guzman', 'date_of_birth': '08/30/2000', 'organization': 'RIT', 'username': 'ddeguzman', 'password': 'in', 'role': 'patient'},
#     {'first_name': 'Cameron', 'last_name': 'Villone', 'date_of_birth': '07/24/2000', 'organization': 'RIT', 'username': 'cvillone', 'password': 'this', 'role': 'patient'},
#     {'first_name': 'Jarrett', 'last_name': 'Bailey', 'date_of_birth': '04/06/2000', 'organization': 'RIT', 'username': 'jbailey', 'password': 'together', 'role': 'physician'},
#     {'first_name': 'Cara', 'last_name': 'Guernsey', 'date_of_birth': '04/06/2000', 'organization': 'RIT', 'username': 'cguernsey', 'password': '!!!', 'role': 'physician'}
# ]
# handler.add_credentials(data)
# # successful log in
# auth = handler.check_credentials('brolly', 'yes')
# # checks for invalid credentials
# if auth:
#     print("authorized")
# else:
#     print("not authorized")
