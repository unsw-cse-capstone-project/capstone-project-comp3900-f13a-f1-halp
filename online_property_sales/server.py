from flask import Flask
# import login manager
# import models
# from models.bidSystem import bidApp

# instantiate app object
app = Flask(__name__)

# cookies
app.secret_key = "*U78u!#2@fs"

# instantiate models
#System = bidApp()