#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
import json

engine = create_engine('postgresql://nailgun:nailgun@localhost/nailgun', echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Ip_addr_ranges(Base):
    __tablename__ = 'ip_addr_ranges'
    
    id = Column(Integer, primary_key=True)
    network_group_id = Column(Integer, ForeignKey('network_groups.id'))
    first = Column(String)
    last = Column(String)
   
    group = relationship("Network_groups", backref=backref('ip_addr_ranges', order_by=id))
 
    def __repr__(self):
        return "%s\t%s\t%s\t%s" % (self.id, self.network_group_id, self.first, self.last)

class Network_groups(Base):
    __tablename__ = 'network_groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    cluster_id = Column(Integer)
    meta = Column(String)

    def __repr__(self):
        return "%s\t%s\t%s\t%s" % (self.id, self.name, self.cluster_id, self.meta)

class Clusters(Base):
    __tablename__ = 'clusters'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "%s\t%s" % (self.id, self.name)

def validIP(address):
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for item in parts:
        if not 0 <= int(item) <= 255:
            return False
    return True

def main():
    session = Session()

    print "Choose ID of your cluster:"
    print "ID\tName"
    id_list = []
    for instance in session.query(Clusters):
        id_list.append(instance.id)
        print instance
    mycluster_id=None
    while mycluster_id not in id_list:
        try:	
            mycluster_id = int(raw_input("answer: "))
        except:
            print "You typed not a correct number"

    print "Current public range:"
    for i, j in session.query(Ip_addr_ranges, Network_groups).join(Network_groups).\
        filter(Network_groups.cluster_id==mycluster_id).filter(Network_groups.name=='public'):
        print "first: " + i.first + "\t" + "last: " + i.last
        meta = json.loads(j.meta)
        new_first = raw_input("type new first: ")
        if validIP(new_first):
            i.first = new_first
            meta["ip_range"][0] = new_first 
	    print "You have changed first ip: " + i.first
        else:
            print "You have typed incorrect value and first ip hasn't changed"
        new_last = raw_input("type new last: ")
        if validIP(new_last):
            i.last = new_last
            meta["ip_range"][1] = new_last 
	    print "You have changed last ip: " + i.last
        else:
            print "You have typed incorrect value and last ip hasn't changed"
        j.meta = json.dumps(meta)
    
    session.commit()

if __name__ == "__main__":
    main()
