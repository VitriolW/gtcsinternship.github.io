from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://user:pass@localhost:3306/dummydata', echo=True)
Base = declarative_base()

########################################################################
class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
#----------------------------------------------------------------------

class Experience(Base):
    __tablename__ = 'experiences'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)  # Modify as needed
    keywords = Column(String(255), nullable=False) # Modify as needed
    description = Column(Text, nullable=False)  # Modify as needed
    uid = Column(Integer, nullable=False) #User id
#----------------------------------------------------------------------

# create tables
Base.metadata.create_all(engine)