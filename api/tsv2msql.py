#https://stackoverflow.com/questions/31394998/using-sqlalchemy-to-load-csv-file-into-a-database
#https://tree.opentreeoflife.org/about/taxonomy-version/ott3.0

from numpy import genfromtxt
from time import time
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Date, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys

def Load_Data(file_name):
    data = genfromtxt(file_name, delimiter='\t', skip_header=1, converters={0: lambda s: str(s)})
    return data.tolist()

Base = declarative_base()

class Tree_of_Life(Base):
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __tablename__ = 'tree_of_life'
    __table_args__ = {'sqlite_autoincrement': True}
    #tell SQLAlchemy the name of column and its attributes:
    id = Column(Integer, primary_key=True, nullable=False)
    uid = Column(Integer)
    parent_uid = Column(Integer)
    name = Column(String)
    rank = Column(String)
    sourceinfo = Column(String)
    uniqname = Column(String)

if __name__ == "__main__":
    t = time()

    #Create the database
    engine = create_engine('sqlite:///tree_of_life.db')
    Base.metadata.create_all(engine)

    #Create the session
    session = sessionmaker()
    session.configure(bind=engine)

    try:
        file_name = sys.argv[1]
        #data = Load_Data(file_name)
        #data = open(file_name).readlines()[1:]

        with open(file_name) as data:
            next(data)
            for i in data:
                s = session()
                j = i.split('\t')
                record = Tree_of_Life(**{
                    'uid': j[0],
                    'parent_uid': j[2],
                    'name': j[4],
                    'rank': j[6],
                    'sourceinfo': j[8],
                    'uniqname': j[10]
                })
                s.add(record) #Add all the records
                s.commit() #Attempt to commit all the records
                s.close() #Close the connection
    except:
        s.rollback() #Rollback the changes on error
    finally:
        s.close() #Close the connection
    print("Time elapsed: " + str(time() - t) + " s.") #0.091s
