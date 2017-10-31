# -*- coding: utf-8 -*-
from parser import Parser

r = Parser()
query = "Does Barrafina provides Halal foods?"

# a = r.define_question_type(query)
r.get_data(query)
# r.get_sql(query)

