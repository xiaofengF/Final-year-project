import unittest
from parser import Parser

class UnitTest(unittest.TestCase):
	# test define_question_type
	def test1(self):
		parser = Parser()
		# for question type 1
		self.assertEqual(parser.define_question_type("what is Barrafina?", [('barrafina', 'title')]), '1')
		# for question type 2
		self.assertEqual(parser.define_question_type("Provide me some good restaurants", [('good', 'goodrate')]), '2')
		# for question type 3
		self.assertEqual(parser.define_question_type("What is the location of dozo?", [('dozo', 'title')]), '3')
		# for question type 4
		self.assertEqual(parser.define_question_type("Does KFC provides sushi?", [('kfc', 'title'),('sushi', 'feature')]), '4')
		# for question type 5
		self.assertEqual(parser.define_question_type("What is the feature of You Me Sushi?", [('you me sushi', 'title'),('feature', 'adjective')]), '5')
	
	# test find_entity
	def test2(self):
		parser = Parser()
		self.assertEqual(parser.find_entity('you me sushi'), ['you me sushi'])
		self.assertEqual(parser.find_entity('the Japanese Canteen'), ['canteen', 'japanese canteen'])
		self.assertEqual(parser.find_entity('give me a Japanese canteen'), ['canteen', 'japanese canteen'])
		self.assertEqual(parser.find_entity('hello'), [])
		self.assertEqual(parser.find_entity('what is kfccc'), [])
	
	# test find_postcode
	def test3(self):
		parser = Parser()
		self.assertEqual(parser.find_postcode('n1c'), 1)
		self.assertEqual(parser.find_postcode('nc'), 0)
		self.assertEqual(parser.find_postcode('we1'), 0)

	# test get_keywords
	def test4(self):
		parser = Parser()
		self.assertEqual(parser.get_keywords('What is the best Burger King in London?'), [('burger king', 'title'),('best','goodrate'), ('london','unknown')])
		self.assertEqual(parser.get_keywords('Are there any chinese restaurants locate in N1C?'), [('restaurants', 'unknown'), ('chinese', 'feature'),('n1c', 'postleft')])

if __name__ == '__main__':
	unittest.main()