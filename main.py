from GlideRecord import *
from Credentials import *

gr = GlideRecord("sys_user")

gr.set_server("https://dev81975.service-now.com")
gr.set_credentials(user, password)

gr.addQuery('name', 'STARTSWITH', 'Emanuel')
gr.query()

gr.deleteMultiple()


# gr.caller_id = "6816f79cc0a8016401c5a33be04be441"
# gr.short_description = "Criando um incident a partir do Python"
# gr.description = "ServiceNow GlideRecord API allows you to Create a record using Python"
# gr.assignment_group = "ServiceNow GlideRecord API allows you to Create a record using Python"
# gr.insert()

