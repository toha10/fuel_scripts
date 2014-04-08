#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://nailgun:nailgun@localhost/nailgun', echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Node(Base):
    __tablename__ = 'nodes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    mac = Column(String)
    
    def __repr__(self):
        return "%s\t%s\t%s" % (self.id, self.name, self.mac) 

class Node_attributes(Base):
    __tablename__ = 'node_attributes'

    id = Column(Integer, primary_key=True)
    node_id = Column(Integer)

session = Session()

print "Choose ID of your node which you want to delete from database:"
print "ID\tNAME\t\t\tMAC"
node_list = []
for instance in session.query(Node):
    node_list.append(instance.id)
    print instance
mynode_id=None
while mynode_id not in node_list:
    try:
        mynode_id = int(raw_input("answer: "))
    except:
        print "You typed not a correct number"

print "You've choosed node-%s. Do you realy want to delete it?" % (mynode_id)

answer = ""
while answer not in ["y", "n"]:
    answer = raw_input("y/n: ")

if answer == "y":
    attrib = session.query(Node_attributes).filter(Node_attributes.node_id == mynode_id).delete()
    node = session.query(Node).filter(Node.id == mynode_id).delete()
    print "node-%s has been deleted" % (mynode_id)


session.commit()
