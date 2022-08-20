from Credentials import *


from GlideRecord import *

gr = GlideRecord("incident")

gr.set_server("https://instace.service-now.com")
gr.set_credentials(user, password)

gr.initialize()

gr.short_description = "Computador reiniciando sozinho!"
gr.category = "hardware"
gr.impact = 1
gr.urgency = 1

gr.insert()



