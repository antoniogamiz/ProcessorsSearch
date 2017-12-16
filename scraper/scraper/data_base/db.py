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
                query="create table FIELD (id int, field1 varchar(100), field2 varchar(100), field3 varchar(100), field4 varchar(100), field5 varchar(100));"
                print(self.cursor.execute(query))
                self.connect.commit()
            except:
                print("Warning: FIELD table, wich is used by this program, is already created.")
            
            return 1
        except:
            return -1

    def getIDs(self):
        query="select ID from FIELD where 1"
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
            query="update FIELD set "+"field1=\""+arg[1]+"\", "+"field2=\""+arg[2]+"\", "+"field3=\""+arg[3]+"\", "+"field4=\""+arg[4]+"\", "+"field5=\""+arg[5]+"\" where id=\""+str(arg[0])+"\";"
            self.cursor.execute(query)
            self.connect.commit()

    def getRegisterWithID(self, id):
        query="select * from FIELD where id="+str(id)+";"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def getRegisters(self):
        query="select * from FIELD where 1;"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def addRegister(self, *arg):
        if len(arg) != 5:
            return -1
        values = "("+str(self.getAvailableID())+",\""+arg[0]+"\",\""+arg[1]+"\",\""+arg[2]+"\",\""+arg[3]+"\",\""+arg[4]+"\");"
        query="insert into FIELD (id, field1, field2, field3, field4, field5) values "+values
        self.cursor.execute(query)
        self.connect.commit()

    def remove(self, index):
        query = "delete from FIELD where id="+str(index)+";"
        self.cursor.execute(query)
        self.connect.commit()

    def clear(self):
        query = "delete from FIELD where 1;"
        self.cursor.execute(query)
        self.connect.commit()