# coding=utf-8

import sys
import mongo as mog
# import traceback

'''receive data form mongoDB'''


class Receiver():
    def __init__(self, port):
        try:
            self.dm = mog.DBMongo(port)
        except Exception as e:
            print(Exception, ':', e)

    def receiver(self, database_name, table_name, target):
        self.dm.connectDB(database_name)
        self.dm.openColl(table_name)
        return self.dm.getInfo(target)


if __name__ == "__main__":

    target = ['wcType', 'unixTime', 'networkMode', 'area', 'adxCode', 'gender', 'price', 'appName', 'mobileOs', 'ip',
              'wcAcId', 'wcOrgBidPrice', 'appMediaCat', 'clicked']
    try:
        mg = Receiver(10001)
        print(mg.receiver('pCTR', 'wuhu', target))
    except Exception as e:
        print(Exception, e)