import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('mysql+pymysql://user:pass@localhost:3306/dummydata', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

dummy1 = Experience()


# commit the record the database
session.commit()

