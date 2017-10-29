# -*- coding: utf-8 -*-
from parser import Parser

r = Parser()
query = "Does Barrafina locate in the centre?"

a = r.define_question_type(query)
# a = r.get_keywords(query)




print(a)
