from typing import overload
from unittest import result
import requests
import base64
import json
import getpass

class GlideRecord:

    __initialize = False

    #Definindo os parâmetros inicias da criação da classe GlideRecord
    def __init__(self, tableName):
        self.query_data = dict()
        self._user = None
        self._password = None
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

    #Implementado "Magic Method" get 
    def __getattr__(self, name):
        return self.results[self.currentIndex][name]

    #Implementado "Magic Method" set 
    def __setattr__(self, name, value):
        #verifica se todas as variáveis inicias foram criadas
        if self.__initialize and name not in self.__dict__:
            #criando objeto para atualizar ou criar um registro
            self.obj[name] = value 
        self.__dict__[name] = value
            

    #setando o endereço da instância
    def set_server(self, servername):
        self.query_data['server'] = servername

    #método para definir as credenciais
    def set_credentials(self, user, password):
        self._user = user
        self._password = password

    #lê a entrada das credenciais do usuário no Servicenow
    def get_credentials(self):
        self._user = input("Digite seu usuário Servicenow: ")
        self._password = getpass.getpass("Digite a sua senha: ")

    #retorna a quantidade registros encontrados ao realizar a query
    def getRowCount(self):
        return len(self.results)

    #retorna um registro específico a partir do sys_id ou do par key e value
    def get(self, *args):
        if(len(args) == 1):
            key = args[0]
            self.query_data['sysparm_query'] = "sys_id="+key
            self.query()
            
            if self.getRowCount() == 1:
                return True
            return False

        else:
            key = args[0]
            value = args[1]

            self.addQuery(key, value)
            self.query_data['limit'] = "1"
            self.query()
            
            if self.getRowCount() > 1:
                return True
            return False

    #verifica se ainda existe algum registro na lista
    def hasNext(self):
        if self.getRowCount() > 0 and self.currentIndex + 1 < self.getRowCount():
            return True
        return False

    #pega o próximo registro da query
    def next(self):
        self.obj = {}
        if self.query_data['rowCount'] > 0 and self.currentIndex + 1 < self.query_data['rowCount']:
            self.currentIndex += 1
            return True
        return False

    #adiciona uma query
    def addQuery(self, *args):
        if(len(args) == 2):
            key = args[0]
            value = args[1]
            if self.query_data['sysparm_query'] == "":
                self.query_data['sysparm_query'] += key +"=" +value
            else:
                self.query_data['sysparm_query'] += "^"+key +"=" +value

        else:
            key = args[0]
            operator = args[1]
            value = args[2]
            if self.query_data['sysparm_query'] == "":
                self.query_data['sysparm_query'] +=  key + operator + value
            else:
                self.query_data['sysparm_query'] += "^" + key + operator + value

    #adiciona uma encoded query
    def addEncodedQuery(self, queryString):
        if self.query_data['sysparm_query'] == "":
            self.query_data['sysparm_query'] = queryString
        else:
            self.query_data['sysparm_query'] += "^" + queryString

    #ordena os resultado a partir de um campo escolhido em ordem crescente
    def orderBy(self, field):
        if self.query_data['sysparm_query'] == "":
            self.query_data['sysparm_query'] = "ORDERBY" + field
        else:
            self.query_data['sysparm_query'] = "^ORDERBY" + field

    #ordena os resultado a partir de um campo escolhido em ordem decrescente
    def orderByDesc(self, field):
        if self.query_data['sysparm_query'] == "":
            self.query_data['sysparm_query'] = "ORDERBYDESC" + field
        else:
            self.query_data['sysparm_query'] = "^ORDERBYDESC" + field

    #manda a query montado para o endpoit da instância através do método GET
    def query(self):
        self.currentIndex = -1
        req = requests.get(
            self.query_data['server']+"/api/now/table/"+self.query_data['tableName']+"?sysparm_query="+
            self.query_data['sysparm_query'] + 
            "^sysparm_display_value=false&sysparm_exclude_reference_link=true&sysparm_limit="+self.query_data['limit'], 
            auth=(self._user, self._password)
        )
        self.results = json.loads(req.content)
        self.results = self.results['result']
        self.query_data['rowCount'] = len(self.results)

    #retorna o value de uma campo específico
    def getValue(self, key):
        rs = self.results[self.currentIndex][key]
        return rs    

    #atualizamos o valor de um campo e a lista de objetos a ser mandando para atualizar o registro
    def setValue(self, field, value=""):
        self.obj[field] = value
        self.results[self.currentIndex] = value

    def setLimit(self, limit):
        self.query_data['limit'] = str(limit)

    #atualizar um registro
    def update(self):
        sys_id = self.results[self.currentIndex]['sys_id']
        data = json.dumps(self.obj)
        req = requests.put(self.query_data['server']+"/api/now/table/"+self.query_data['tableName']+"/"+sys_id, auth=(self._user, self._password), data=data)
        print(req.status_code)
        print(req.content)

    #resetando dicionário para inserir um novo registro na tabela
    def initialize(self):
        self.obj = {}
        
    #inserindo um novo registro na tabela
    def insert(self):
        data = json.dumps(self.obj)
        req = requests.post(self.query_data['server']+"/api/now/table/"+self.query_data['tableName'] + "?sysparm_display_value=false&sysparm_exclude_reference_link=true", 
        auth=(self._user, self._password), data=data)
        print(req.status_code)
        print(req.content)

        results = json.loads(req.content)
        self.results = []
        self.results.append(results['result'])
        self.currentIndex = 0
        self.query_data['rowCount'] = 0

    #pesquisa se um determinado registro existe a partir de um campo e seu valor
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
        req = requests.delete(self.query_data['server']+"/api/now/table/"+self.query_data['tableName']+"/"+sys_id, auth=(self._user, self._password))
        print(req.status_code)
        print(req.content)


    def deleteMultiple(self):
        for record in self.results:
            sys_id = record['sys_id']
            self.delete(sys_id)
           
