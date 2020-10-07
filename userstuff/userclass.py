from flask_login import UserMixin
from bankDetails import BankDetails

#buyers and sellers all have to add extral bank details as some point, and all their attributes are the same,
#So I just treat them all as users, They just need to input the extral details at different time. 
#It is not clearified that if one user should have only 1 or more bank cards, so I treat band details as a class
#and only need to justify a user keep one or a list of bank account

#The difference is that buyers need to register initial bids for properties
#If user keeps the initial bids as an attribute, he/she has to keep a list of initial bids and cooresponding property(ID)
#Or should the property keeps a list of registered auction buyers(RAB) with their cooresponding initial bids 
class User(UserMixin):
    def __init__(self,login_name, password, address, date_of_birth):
        self._login_name = login_name
        self._password = password
        self._address= address
        self._date_of_birth = date_of_birth
        # self._bank_details = None

        self.id = login_name
    
    @property
    def login_name (self):
        return self._login_name

    @property
    def password (self):
        return self._password
    
    @property
    def address (self):
        return self._address
    
    @property
    def date_of_birth (self):
        return self._date_of_birth
    
    @property
    def bank_details (self):
        return self._bank_details
    
    @login_name.setter
    def login_name(self, value):
        self._login_name=value

    @password.setter
    def password(self, value):
        self._password=value

    @address.setter
    def address(self, value):
        self._address=value

    @date_of_birth.setter
    def date_of_birth(self, value):
        self._date_of_birth=value
    
    @bank_details.setter
    def bank_details(self, value):
        self._bank_details = value

    def __str__(self):
        return self._login_name + "  " + self._password + " " + self._address + " " + self._date_of_birth

# class Seller(User):
#     def __init__(self,login_name, password, address, dateOfBirth, phone_number, id_confirmation, card_number, holder_fname, holder_lname, cvc, expire_date):
#         super().__init__(login_name, password, address, dateOfBirth)
#         self._phone_number = phone_number
#         self._id_confirmation = id_confirmation
#         self._card_number = card_number
#         self._holder_fname = holder_fname
#         self._holder_lname = holder_lname
#         self._cvc = cvc
#         self._expire_date = expire_date

#         @phone_number.setter
#         def phone_number(self, value):
#             self._phone_number=value

#         @id_confirmation.setter
#         def id_confirmation(self, value):
#             self._id_confirmation=value

#         @card_number.setter
#         def card_number(self, value):
#             self._card_number=value

#         @holder_fname.setter
#         def holder_fname(self, value):
#             self._holder_fname=value

#         @holder_lname.setter
#         def holder_lname(self, value):
#             self._holder_lname=value

#         @cvc.setter
#         def cvc(self, value):
#             self._cvc=value

#         @expire_date.setter
#         def expire_date(self, value):
#             self._expire_date=value


print("wwwwwww")
tom = User("Tom","password","address", "05/22")
b = BankDetails("1888888888","EV354","1111 2222 3333 4444","fname","lname","123","10/2020")
tom.bank_details= b
print(tom)
print(tom.bank_details)
