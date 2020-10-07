from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date
class BankDetails:
    def __init__ (self, phone_number, id_confirmation, card_number, holder_fname, holder_lname, cvc, expire_date):
        self._phone_number = phone_number
        self._id_confirmation = id_confirmation
        self._card_number = card_number
        self._holder_fname = holder_fname
        self._holder_lname = holder_lname
        self._cvc = cvc
        self._expire_date = expire_date

    @property
    def phone_number (self):
        return self._phone_number

    @property
    def id_confirmation (self):
        return self._id_confirmation
    
    @property
    def card_number (self):
        return self._card_number
    
    @property
    def holder_fname (self):
        return self._holder_fname

    @property
    def holder_lname (self):
        return self._holder_lname

    @property
    def cvc (self):
        return self._cvc

    @property
    def expire_date (self):
        return self._expire_date
    
    @phone_number.setter
    def phone_number(self, value):
        self._phone_number=value

    @id_confirmation.setter
    def id_confirmation(self, value):
        self._id_confirmation=value

    @card_number.setter
    def card_number(self, value):
        self._card_number=value

    @holder_fname.setter
    def holder_fname(self, value):
        self._holder_fname=value

    @holder_lname.setter
    def holder_lname(self, value):
        self._holder_lname=value

    @cvc.setter
    def cvc(self, value):
        self._cvc=value

    @expire_date.setter
    def expire_date(self, value):
        self._expire_date=value
    
    def __str__ (self):
        return self._phone_number+ " " + self._id_confirmation +" "+ self._card_number+" "+ self._holder_fname+" "+ self._holder_lname+ " "+ self._cvc+" "+ self._expire_date

def init_db():
    engine = create_engine('sqlite:///bank.db', echo = True)
    meta = MetaData()
    bank = Table(
        'bank', meta, 
        Column('user_name', String, primary_key = True, Foreign),
        Column('phone_number', Integer), 
        Column('id_confirmation', String),
        Column('card_number',Integer),
        Column('holder_fname', String), 
        Column('holder_lname', String),
        Column('cvc',Integer),
        Column('expire_date', Date)
        # Column('bank_details',object)
        )
    meta.create_all(engine)
    return bank
bank=init_db()