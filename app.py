from flask import Flask,jsonify,request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields,validate, ValidationError
from sqlalchemy.orm import relationship
from sqlalchemy import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= 'mysql+mysqlconnector://root:password@localhost_video_search_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

#<--------------------------------SQL Table Classes----------------------------------->


#<--------------------------------Schema Tables--------------------------------------->


#<--------------------------------Home Page------------------------------------------->

@app.route('/')
def home():
  return 'Welcome to Video Finder'



#<--------------------------------End Routes------------------------------------------>



#<------------------------------------------------------------------------------------>

if __name__ == '__main__':
  app.run(debug=True)