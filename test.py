from parser import Parser

r = Parser()
query = "What is the best You Me sushi in London"

a = r.get_keywords(query)

# print(r.define_question_type(query))




print(a)
