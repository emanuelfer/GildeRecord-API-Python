from unittest import result
import requests
import base64
import json
import re
import getpass
import sys
import time

class GlideRecord:

    __initialize = False

    #Definindo os parâmetros inicias da criação da classe GlideRecord
    def __init__(self, tableName):
        self.query_data = dict()
        self.user_name = None
        self.password = None
        self.obj = dict()

        self.encodedAuth = None
        self.query_data['server'] = None
        self.query_data['tableName'] = tableName
        self.query_data['actionType'] = "getRecords"
        self.results = {}
        self.currentIndex = -1
        self.query_data['rowCount'] = 100
        self.query_data['sysparm_query'] = ""
        self.query_data['limit'] = "100"
        self.__initialize = True
        self.operator = ['IN','NOT IN','STARTSWITH','ENDSWITH','CONTAINS','DOES NOT CONTAIN','INSTANCEOF']

    def __getattr__(self, name):
        return self.results[self.currentIndex][name]

    def __setattr__(self, name, value):
        if self.__initialize and name not in self.__dict__:
            self.obj[name] = value
        self.__dict__[name] = value
            

    #setando o endereço da instância
    def set_server(self, servername):
        self.query_data['server'] = servername

    def set_credentials(self, user_name, password):
        self.user_name = user_name
        self.password = password
        self.reset_credentials()

    #lê a entrada das credenciais do usuário no Servicenow
    def get_credentials(self):
        self.user_name = input("Digite seu usuário Servicenow: ")
        self.password = getpass.getpass("Digite a sua senha: ")
        self.reset_credentials()


    def reset_credentials(self):
        string = self.user_name + ":" + self.password
        self.encodedAuth = base64.b64encode(
            string.encode()
        )

    def getRowCount(self):
        return len(self.results)

    def get(self, key, value):
        self.addQuery(key, value)
        self.setRowCount(1)
        self.query()
        
        if self.getRowCount() == 1:
            return True
        return False

    def hasNext(self):
        if self.getRowCount() > 0 and self.currentIndex + 1 < self.getRowCount():
            return True
        return False

    def next(self):
        self.obj = {}
        if self.query_data['rowCount'] > 0 and self.currentIndex + 1 < self.query_data['rowCount']:
            self.currentIndex += 1
            return True
        return False

    def addQuery(self, key, value=""):
        self.query_data['sysparm_query'] += key +"=" +value

    def addQuery(self, key, operator, value=""):

        if self.query_data['sysparm_query'] == "":
            self.query_data['sysparm_query'] +=  key + operator + value
        else:
            self.query_data['sysparm_query'] += "^" + key + operator + value

    def addEncodedQuery(self, queryString):
        if self.query_data['sysparm_query'] == "":
            self.query_data['sysparm_query'] = queryString
        else:
            self.query_data['sysparm_query'] += "^" + queryString

    def orderBy(self, field):
        if self.query_data['sysparm_query'] == "":
            self.query_data['sysparm_query'] = "ORDERBY" + field
        else:
            self.query_data['sysparm_query'] = "^ORDERBY" + field

    def orderByDesc(self, field):
        if self.query_data['sysparm_query'] == "":
            self.query_data['sysparm_query'] = "ORDERBYDESC" + field
        else:
            self.query_data['sysparm_query'] = "^ORDERBYDESC" + field

    def query(self):
        self.currentIndex = -1
        req = requests.get(
            self.query_data['server']+"/api/now/table/"+self.query_data['tableName']+"?sysparm_query="+
            self.query_data['sysparm_query'] + 
            "^sysparm_display_value=false&sysparm_exclude_reference_link=true&sysparm_limit="+self.query_data['limit'], 
            auth=(self.user_name, self.password)
        )
        self.results = json.loads(req.content)
        self.results = self.results['result']
        self.query_data['rowCount'] = len(self.results)

    def getValue(self, key):
        rs = self.results[self.currentIndex][key]
        return rs    

    def getValue(self, key, value=""):
        self.results[self.currentIndex][key] = value

    def setValue(self, field, value=""):
        self.obj[field] = value
        self.results[self.currentIndex] = value

    def setLimit(self, limit):
        self.query_data['limit'] = str(limit)


    def update(self):
        sys_id = self.results[self.currentIndex]['sys_id']
        data = json.dumps(self.obj)
        req = requests.put(self.query_data['server']+"/api/now/table/"+self.query_data['tableName']+"/"+sys_id, auth=(self.user_name, self.password), data=data)
        print(req.status_code)
        print(req.content)

        
    def insert(self):
        data = json.dumps(self.obj)
        
        req = requests.post(self.query_data['server']+"/api/now/table/"+self.query_data['tableName'], auth=(self.user_name, self.password), data=data)
        print(req.status_code)
        print(req.content)

    def find(self, field, value):
        for index, record in enumerate(self.results):
            if record[field] == value:
                self.currentIndex = index
                return True
        return False

    def deleteRecord(self):
        sys_id = self.results[self.currentIndex]['sys_id']
        self.delete(sys_id)

    def delete(self, sys_id):
        req = requests.delete(self.query_data['server']+"/api/now/table/"+self.query_data['tableName']+"/"+sys_id, auth=(self.user_name, self.password))
        print(req.status_code)
        print(req.content)


    def deleteMultiple(self):
        for record in self.results:
            sys_id = record['sys_id']
            self.delete(sys_id)
           
