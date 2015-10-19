#coding=utf-8

'''
Created on 2015年10月14日

@author: kevin
'''

import sys
import MySQLdb

reload(sys)
# sys.setdefaultencoding('utf-8')

class CrossDbJoiner(object):
    def __init__(self):
        self.dbConfDict1 = {'host' : '10.0.44.11', 'user' : 'gazer', 'passwd' : 'sunlight', 'port' : 3306, 'db' : 'xyqb', 'charset' : 'utf8'}
        self.dbConfDict2 = {'host' : '10.0.44.11', 'user' : 'gazer', 'passwd' : 'sunlight', 'port' : 3307, 'db' : 'risk_control', 'charset' : 'utf8'}
        self.dbPool = {}
        self.joinResultList = []
    
    def initDb(self, dbConfDict1 = {}, dbConfDict2 = {}):
        if (len(dbConfDict1) != 0):
            self.dbConfDict1 = dbConfDict1
        if (len(dbConfDict2) != 0):
            self.dbConfDict2 = dbConfDict2
         
        dbConn1 = MySQLdb.connect(host=self.dbConfDict1.get('host'), user=self.dbConfDict1.get('user'),\
                passwd=self.dbConfDict1.get('passwd'), port = self.dbConfDict1.get('port'), db=self.dbConfDict1.get('db'), charset=self.dbConfDict1.get('charset')) 
        dbConn2 = MySQLdb.connect(host=self.dbConfDict2.get('host'), user=self.dbConfDict2.get('user'),\
                passwd=self.dbConfDict2.get('passwd'), port = self.dbConfDict2.get('port'), db=self.dbConfDict2.get('db'), charset=self.dbConfDict2.get('charset'))    
        cursor1 = dbConn1.cursor() 
        cursor2 = dbConn2.cursor()
        self.dbPool['db1'] = cursor1
        self.dbPool['db2'] = cursor2

    def join(self, sql1, sql2, joinKeyPos = 0):
        resultDict1 = self._select(self.dbPool.get('db1'), sql1, joinKeyPos)
        resultDict2 = self._select(self.dbPool.get('db2'), sql2, joinKeyPos)
        
        if len(resultDict1) == 0 or len(resultDict2) == 0:
            return None
        
        if len(resultDict1) > len(resultDict2):
            return self._joinResult(resultDict1, resultDict2, joinKeyPos, 1)
        else:
            return self._joinResult(resultDict2, resultDict1, joinKeyPos, -1)
                
    def _select(self, cursor, sql, joinKeyPos = 0):
        resultDict = {}
        cursor.execute(sql)      
        for row in cursor.fetchall():      
            resultDict[row[joinKeyPos]] = row       
        return resultDict
    
    def _joinResult(self, resultDict1, resultDict2, joinKey, direction):
        joinResultList = []
        if direction == 1:
            for (key, value) in resultDict1.items():
                value2 = resultDict2.get(key)
                if value2 is not None:
                    rowList = []
                    for item in value:
                        rowList.append(item)
                    length = len(value2)
                    for i in range(1, length):
                        rowList.append(value2[i])
                    joinResultList.append(rowList)
        else:
            for (key, value) in resultDict1.items():
                value2 = resultDict2.get(key)
                if value2 is not None:
                    rowList = []
                    for item in value2:
                        rowList.append(item)
                    length = len(value)
                    for i in range(1, length):
                        rowList.append(value[i])
                    joinResultList.append(rowList)
        self.joinResultList = joinResultList            
        return joinResultList
    
    def saveResult(self, fileName, headLine = ''):
        if self.joinResultList is None:
            print "join result is None!"
            return
        
        with open(fileName, 'w') as fp:
            if (headLine != ''):
                fp.write(headLine + '\n')
            for joinResult in self.joinResultList:
                length = len(joinResult)
                if length == 1:
                    fp.write(str(joinResult[0]) + '\n')  
                elif length > 1:
                    line = str(joinResult[0])
                    for i in range(1, length):
                        line += ',' + str(joinResult[i])
                    print line
                    fp.write(line + "\n")

if __name__=="__main__":
    crossDbJoiner = CrossDbJoiner()
    crossDbJoiner.initDb()
    sql1 = 'SELECT  `loan_application_history_id` , `transaction_status` FROM `loan_application_manifest_history` LIMIT 10000'
    sql2 = 'SELECT `application_no` as loan_application_history_id,NAME,phone_no FROM `ma_shang_jin_rong_feedback` LIMIT 10000'
    crossDbJoiner.join(sql1, sql2)
    crossDbJoiner.saveResult('E:\\sqlresult1.csv', 'id,status,name,phoneno')
