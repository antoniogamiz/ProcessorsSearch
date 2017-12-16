# -*- coding: utf-8 -*-

import MySQLdb

class DB_Handler():
    def openDB(self, **arg):
        if(len(arg)!=4):
            return -1
        try:
            self.connect = MySQLdb.connect(host=arg['host'], user=arg['user'], passwd=arg['passwd'], db=arg['db'])
            self.cursor = self.connect.cursor()
            self.host=arg['host']
            self.user=arg['user']
            self.passwd=arg['passwd']
            self.db=arg['db']
            
            try:
                query="create table PROCESSORS (id int, brand varchar(100), model varchar(100), frequency varchar(100), price int, availability varchar(100));"
                print(self.cursor.execute(query))
                self.connect.commit()
            except:
                print("Warning: PROCESSORS table, wich is used by this program, is already created.")
            
            return 0
        except:
            return -2

    def getIDs(self):
        query="select ID from PROCESSORS where 1"
        self.cursor.execute(query)
        ids = self.cursor.fetchall()

        ids_=[]

        for p in ids:
            ids_.append(p[0])

        return ids_

    def getAvailableID(self):
        ids=self.getIDs()

        i=1
        while i in ids:
            i+=1

        return i

    def editRegisterWithID(self, *arg):
        if len(arg)==6:
            query="update PROCESSORS set "+"brand=\""+arg[1]+"\", "+"model=\""+arg[2]+"\", "+"frequency=\""+arg[3]+"\", "+"price=\""+str(arg[4])+"availability=\""+str(arg[5])+"\" where id=\""+str(arg[0])+"\";"
            self.cursor.execute(query)
            self.connect.commit()

    def getRegisterWithID(self, id):
        query="select * from PROCESSORS where id="+str(id)+";"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def getRegisters(self):
        query="select * from PROCESSORS where 1;"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def addRegister(self, *arg):
        if len(arg) != 5:
            return -1
        values = "("+str(self.getAvailableID())+",\""+arg[0]+"\",\""+arg[1]+"\",\""+arg[2]+"\",\""+str(arg[3])+"\",\""+arg[4]+"\");"
        query="insert into PROCESSORS (id, brand, model, frequency, price, availability) values "+values
        self.cursor.execute(query)
        self.connect.commit()

    def remove(self, index):
        query = "delete from PROCESSORS where id="+str(index)+";"
        self.cursor.execute(query)
        self.connect.commit()

    def clear(self):
        query = "delete from PROCESSORS where 1;"
        self.cursor.execute(query)
        self.connect.commit()

