# -*- coding: utf-8 -*-
from parser import Parser

r = Parser()
query = "Provide me the feature information of Barrafina. "

# a = r.define_question_type(query)
r.get_data(query)
# r.get_sql(query)

