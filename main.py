from GlideRecord import *

gr = GlideRecord("incident")

gr.set_server("https://dev81975.service-now.com")
gr.set_credentials('admin', '=h4@K1oxKcSN')

gr.addQuery('caller_id','=', '77ad8176731313005754660c4cf6a7de')
gr.orderByDesc('number')

gr.query()
print(gr.getRowCount())
while gr.next():
    print(gr.number)

# gr.caller_id = "6816f79cc0a8016401c5a33be04be441"
# gr.short_description = "Criando um incident a partir do Python"
# gr.description = "ServiceNow GlideRecord API allows you to Create a record using Python"
# gr.assignment_group = "ServiceNow GlideRecord API allows you to Create a record using Python"
# gr.insert()

