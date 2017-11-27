# -*- coding: utf-8 -*-
from parser import Parser

r = Parser()
query = "show me the information of the Japanese Canteen"

# a = r.define_question_type(query)
print(r.get_data(query))
# r.get_sql(query)

