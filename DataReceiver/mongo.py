# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from pymongo import MongoClient

class DBMongo():
    def __init__(self, port=10001):
        #self.ip = 'localhost'
        self.ip = '192.168.1.10'
        self.port = int(port)

        self.client = MongoClient(self.ip, self.port)
    
    def connectDB(self, dbName):
        try:
            self.db = self.client[dbName]
        except IOError:
            print 'no such database named %s' % dbName

    def openColl(self, collName):
        self.coll = self.db[collName]

    def getInfo(self, target):
        self.modelConf = { }
        for x in target:
            self.modelConf[x] = 1
        self.modelConf['_id'] = 0 # disable mongo's id
        self.res = { }

        for rec in self.coll.find({}, self.modelConf):
            for (k, v) in rec.items():
                if k == 'area':
                    v = v.replace(' ', ',') # format region (province,city)

                if k in self.res.keys():
                    self.res[k].append(v)
                else:
                    self.res[k] = [ ]
                    self.res[k].append(v)
        return self.res
        
    def printRes(self):
        for (k, v) in self.res.items():
            print k, len(v)

def usage():
    print 'usage: ', 'python mongo.py port'

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        exit(-1)
    target = ["unixTime", "networkMode", "mobileOs", "appMediaCat"]
    dm = DBMongo(sys.argv[1])
    dm.connectDB('pCTR')
    dm.openColl('wuhu')
    dm.getInfo(target)
    dm.printRes()
