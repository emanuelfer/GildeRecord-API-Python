# GildeRecord-API-Python
<h1 align="center"> Implementado a API GlideRecord do Servicenow em Python </h1>

<p>
 Uma das principais APIs para quem desenvolve dentro do Servicenow é a GlideRecord. Ele nos permite fazer queries, criar e atualizar registros, além de inúmeras outras funções. Assim, levado pela curiosidade de como seria uma possível implementação dessa classe, resolvi tentar uma implementação bem simplificada utilizando python e como base de dados a minha instância pessoal do Servicenow, consumindo a API REST.
 
 Com essa implementação, temos as seguintes possibilidades:
 <ul>
  <li>Realizar a query de registros nas tabelas</li>
  <li>Criar novos registros</li>
  <li>Atualizar registros</li>
  <li>Deletar registros únicos ou todos os registros filtrados</li>
 <ul>
  
  <hr></hr>
  
  <p> Seguem alguns exemplos de como utilizar as funções: </p>
  
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
  
 </p>
