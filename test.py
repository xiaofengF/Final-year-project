# -*- coding: utf-8 -*-
from parser import Parser

r = Parser()
query = "GIVE ME THE BEST CHINESE RESTAURANT IN N1C."

# a = r.define_question_type(query)
a = r.get_sql(query)

print(a)

