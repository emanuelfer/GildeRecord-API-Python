# GildeRecord-API-Python
<h1 align="center"> Implementado a API GlideRecord do Servicenow em Python </h1>

<p>
 Uma das principais APIs para quem desenvolve dentro do Servicenow é a GlideRecord. Ele nos permite fazer queries, criar e atualizar registros, além de inúmeras outras funções. Assim, levado pela curiosidade de como seria uma possível implementação dessa classe, resolvi tentar recriá-la, de forma bem simplificada, utilizando python e como base de dados a minha instância pessoal do Servicenow, consumindo a API REST.</p>
 
 Com essa implementação, temos as seguintes possibilidades:
 <ul>
  <li>Realizar a query de registros nas tabelas</li>
  <li>Criar novos registros</li>
  <li>Atualizar registros</li>
  <li>Deletar registros únicos ou todos os registros filtrados</li>
 <ul>
  
<hr></hr>
  
<h4>Seguem alguns exemplos de como utilizar as funções:</h4>
  
Lendo registros de uma tabela
  
  
```python
  
from GlideRecord import *

gr = GlideRecord("incident")

gr.set_server("https://instance.service-now.com")
gr.set_credentials(user, password)

gr.addQuery('assignment_group.name', 'Hardware')
gr.query()

while gr.next():
    print(gr.number)

```
  
  
Atualizando registros de uma tabela
 
```python
  
from GlideRecord import *

gr = GlideRecord("incident")

gr.set_server("https://instance.service-now.com")
gr.set_credentials(user, password)

gr.addQuery('number', 'INC0000051')
gr.query()

if gr.next():
    gr.short_description = "Sem conexão de internet!"
    gr.update()

```
  
Criando um novo incident
 
```python
  
from GlideRecord import *

gr = GlideRecord("incident")

gr.set_server("https://dev81975.service-now.com")
gr.set_credentials(user, password)

gr.initialize()

gr.short_description = "Computador reiniciando sozinho!"
gr.category = "hardware"
gr.impact = 1
gr.urgency = 1

gr.insert()

```
 
 
<p>
Esta é a apenas a primeira versão, ainda existem melhorias a serem feitas e nem todas as funções da API GlideRecord foram implementadas, apenas as principais. Para mais informações sobre a API oficial, segue a documentação:
 
https://developer.servicenow.com/dev.do#!/reference/api/rome/server_legacy/c_GlideRecordAPI#r_GlideRecord-initialize?navFilter=gliderecord
 
Material utilizado como referência:
https://github.com/bazizi/ServiceNow_GlideRecord_API
https://github.com/sfu/php-gliderecord/blob/master/src/GlideRecord.php
 
</p>
  


  


  
