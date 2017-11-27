# -*- coding: utf-8 -*-
from __future__ import division
import string
from itertools import groupby
import nltk
from nltk.tokenize import wordpunct_tokenize
from PyDictionary import PyDictionary
import MySQLdb
from nltk import pos_tag

class Parser(object):

    def __init__(self, stopwords=None, punctuations=None, language='english'):
        self.stopwords = stopwords
        if self.stopwords is None:
            self.stopwords = nltk.corpus.stopwords.words(language)

        self.punctuations = punctuations
        if self.punctuations is None:
            self.punctuations = list(string.punctuation)

        self.to_ignore = set(self.stopwords + self.punctuations)

    def get_data(self, query):
        query = self.get_sql(query)
        if query == None:
            return None
        db = MySQLdb.connect(host='localhost', user='root',passwd='961127',db='django')
        cursor = db.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        db.close()
        print query
        return results

    def get_sql(self, query):
        keywords = self.get_keywords(query)
        if keywords == None:
            return None
        keywords = [word for word in keywords if word[1] != "unknown"]
        print keywords
        if keywords == []:
            return None
        question_type = self.define_question_type(query, keywords)
        print question_type
        sql = ""
        if question_type == "1":
            sql = "SELECT * FROM Restaurants_data WHERE "
            include_rate = 0

            for keyword in keywords:
                if keyword[1] == 'badrate':
                    sql += "rate = (SELECT max(rate) FROM Restaurants_data WHERE "
                    include_rate = 1
                elif keyword[1] == 'goodrate':
                    sql += "rate = (SELECT min(rate) FROM Restaurants_data WHERE "
                    include_rate = 1

            sql = self.sql2(keywords, sql)
            if sql[-6:-1] == "WHERE":
                sql = sql[:-6]
            if include_rate == 1:
                sql += ")"
        elif question_type == "2":
            sql = "SELECT * FROM Restaurants_data WHERE "
            sql = self.sql2(keywords, sql)
            if sql[-6:-1] == "WHERE":
                sql = sql[:-7]

            for keyword in keywords:
                if keyword[1] == 'badrate':
                    sql += " ORDER BY rate DESC"
                elif keyword[1] == 'goodrate':
                    sql += " ORDER BY rate"
        elif question_type == "3":
            sql = "SELECT location FROM Restaurants_data WHERE " 
            sql = self.sql2(keywords, sql)
            sql += " GROUP BY location"
            if sql == "SELECT location FROM Restaurants_data WHERE  GROUP BY location":
                return None
        elif question_type == "4":
            sql = "SELECT * FROM Restaurants_data WHERE "
            sql = self.sql2(keywords, sql)
            if sql == "SELECT * FROM Restaurants_data WHERE ":
                return None
        elif question_type == "5":
            sql = "SELECT "
            for keyword in keywords:
                if keyword[1] == 'phone':
                    sql += "phone FROM Restaurants_data WHERE "
                    sql = self.sql2(keywords, sql)
                    sql += " GROUP BY phone"
                    break
                elif keyword[1] == 'speciality':
                    sql += "feature FROM Restaurants_data WHERE "
                    sql = self.sql2(keywords, sql)
                    sql += " GROUP BY feature"
                    break
            if sql == "SELECT ":
                return None
        print sql
        return sql

    def sql(self, keyword, sql):
        sql = "'"
        sql += keyword[0]
        sql += "'"
        return sql

    def sql2(self, keywords, sql):
        limit = 0
        for keyword in keywords:
            if limit != 0:
                sql += " AND "
            if keyword[1] == 'title':
                sql += "title like "
                sql += self.sql(keyword, sql)
                limit += 1
            elif keyword[1] == 'price':
                sql += "price like "
                sql += self.sql(keyword, sql)
                limit += 1
            elif keyword[1] == 'feature':
                sql += "feature like "
                sql += self.sql(keyword, sql)
                limit += 1
            elif keyword[1] == 'postleft':
                sql += "postLeft like "
                sql += self.sql(keyword, sql)
                limit += 1

            if sql[-4:-1] == "AND":
                sql = sql[:-5]
        return sql

    def get_synonyms(self, wordSet, dictionary):
        new_word = []
        for word in wordSet:
            li = dictionary.synonym(word)
            if not li == None:
                for l in li:
                    new_word.append(l)
        wordSet.update(new_word)
        return wordSet

    def get_keywords(self, text):
        sentence = nltk.tokenize.sent_tokenize(text)
        if sentence == []:
            return None
        for s in sentence:
            parameter = self.generate_phrases(s)
            if type(parameter)==list:
                phrase_list = parameter[1]
                entity = parameter[0]
            else:
                phrase_list = parameter
        keywords = []
        for phrase in phrase_list:
            keywords.append(' '.join(phrase))
        tup = []
        features = [word.lower() for word in ['Afghani','African','Albanian','American','Arabic','Argentinean','Armenian','Asian','Australian','Austrian','Balti','Bangladeshi','Bar','Barbecue','Belgian','Brazilian','Brew Pub','British','Burmese','Cafe','Cajun & Creole','Cambodian','Canadian','Caribbean','Central American','Central Asian','Central European','Chilean','Chinese','Colombian','Contemporary','Croatian','Cuban','Czech','Danish','Delicatessen','Diner','Dutch','Eastern European','Ecuadorean','Egyptian','Ethiopian','European','Fast Food','Filipino','French','Fusion','Gastropub','Georgian','German','Gluten Free Options','Greek','Grill','Halal','Hawaiian','Healthy','Hungarian','Indian','Indonesian','International','Irish','Israeli','Italian','Jamaican','Japanese','Korean','Kosher','Latin','Latvian','Lebanese','Malaysian','Mediterranean','Mexican','Middle Eastern','Minority Chinese','Moroccan','Nepali','New Zealand','Norwegian','Pakistani','Persian','Peruvian','Pizza','Polish','Polynesian','Portuguese','Pub','Romanian','Russian','Salvadoran','Scandinavian','Scottish','Seafood','Singaporean','Soups','South American','Southwestern','Spanish','Sri Lankan','Steakhouse','Street Food','Sushi','Swedish','Swiss','Taiwanese','Thai','Tibetan','Tunisian','Turkish','Ukrainian','Uzbek','Vegan Options','Vegetarian Friendly','Venezuelan','Vietnamese','Welsh','Wine Bar']]

        # synonyms  
        dictionary = PyDictionary()
        good = self.get_synonyms(set(['good', 'popular', 'well-known','best','top','great']), dictionary)
        expensive = self.get_synonyms(set(['expensive']), dictionary)
        cheap = self.get_synonyms(set(['cheap']), dictionary)
        bad = self.get_synonyms(set(['bad', 'worse','worst']), dictionary)
        feature = self.get_synonyms(set(['speciality', 'feature', 'features']), dictionary)
        phone = self.get_synonyms(set(['phone','telephone','contact','mobile-phone']), dictionary)

        for keyword in keywords:
        # price
            word = keyword
            if keyword in expensive:
                keyword = ('$$$$', 'price', word)
            elif keyword in cheap:
                keyword = ('$', 'price', word)
        # feature
            elif keyword in features:
                keyword = (keyword, 'feature')
            elif keyword in feature:
                keyword = (keyword, 'speciality')
            elif keyword in phone:
                keyword = (keyword, 'phone')
        # rate
            elif keyword in good:
                keyword = (keyword, 'goodrate')
            elif keyword in bad:
                keyword = (keyword, 'badrate')
        # postLeft
            elif self.find_postcode(keyword):
                keyword = (keyword, 'postleft')
        # title
            elif keyword == 'entity':
                keyword = (entity, 'title')
            else:
                keyword = (keyword, 'unknown')
            tup.append(keyword)
        return tup

    def find_postcode(self, keyword):
        # Get postcode
        db = MySQLdb.connect(host='localhost', user='root',passwd='961127',db='django')
        cursor = db.cursor()
        cursor.execute("SELECT postLeft FROM Restaurants_data GROUP BY postLeft")
        results = cursor.fetchall()
        db.close()

        for result in results:
            post = result[0].lower()
            if keyword == post:
                return 1
        return 0

    def find_entity(self, sentence):
        # identify the entity in a sentence
        db = MySQLdb.connect(host='localhost', user='root',passwd='961127',db='django')
        cursor = db.cursor()
        cursor.execute("SELECT title FROM Restaurants_data GROUP BY title")
        results = cursor.fetchall()
        db.close()
        title_list = []
        potential_entities = []
        sentence = sentence.replace('the','') + ' '

        # Find potential entities
        for result in results:
            title = result[0].lower()
            title_list.append(title)

        for t in title_list:
            if sentence.lower().find(t) != -1:
                potential_entities.append(t)  

        # Delete wrong entities
        potential_entities = [x for x in potential_entities if not (sentence[sentence.lower().find(x) - 1].isalpha() or sentence[sentence.lower().find(x) + len(x)].isalpha())]
        return potential_entities

    # change format
    def change_format(self, text):
        if text.find("I'm") != -1:
            sentence = nltk.tokenize.sent_tokenize(text.replace("I'm", "I am"))
        elif text.find("What's") != -1:
            sentence = nltk.tokenize.sent_tokenize(text.replace("What's", "What is"))
        elif text.find("Where's") != -1:
            sentence = nltk.tokenize.sent_tokenize(text.replace("Where's", "Where is"))
        elif text.find("What're") != -1:
            sentence = nltk.tokenize.sent_tokenize(text.replace("What're", "What are"))
        elif text.find("Where're") != -1:
            sentence = nltk.tokenize.sent_tokenize(text.replace("Where're", "Where are"))
        else:
            sentence = nltk.tokenize.sent_tokenize(text)
        return sentence

    def generate_phrases(self, sentence):
        phrase_list = set()
        potential_entities = self.find_entity(sentence)
        
        sentence = self.change_format(sentence)
        for s in sentence:
            word_list = [word.lower() for word in wordpunct_tokenize(s)]

        # The longest one will be identified to a entity
        if potential_entities:
            entity = max(potential_entities, key = len)
            for s in sentence:
                s = s.lower().replace(entity, 'entity')
                word_list = wordpunct_tokenize(s)

        tagged = pos_tag(word_list)

        # Delete verb in the query
        for w, t in zip(word_list,tagged):
            if t[1] in ['VB', 'VBG', 'VBD','VBN','VBP','VBZ'] or t[0] == 'list':
                word_list.remove(w)
        phrase_list.update(self.get_phrases(word_list, tagged))
        
        if 'entity' in dir():
            parameter = [entity, phrase_list]
            return parameter
        else:
            return phrase_list
   
    def get_phrases(self, word_list, tagged):
        phrase_list = []
        for group in groupby(word_list, lambda x: x in self.to_ignore):
            if not group[0]:
                l = list(group[1])
                new_tagged= []
                for tag in tagged:
                    for word in l:
                        if word == tag[0]:
                            new_tagged.append(tag)
                # seperate adjective words
                for w, t in zip(l, new_tagged):
                    if t[1] in ['JJ','JJR','JJS','RBS','RB','RBR'] or  not (t[0].find('ese') == -1):
                        l.remove(w)
                        adjective = (t[0], )
                        phrase_list.append(adjective)
                if l != []:
                    for word in l:
                        w = (word, )
                        phrase_list.append(w)
        return phrase_list

    def calculate_probability(self, answers, query_length, query_list):
        # Calculate
        probability_set = []
        for answer in answers:
            answer_list = answer['queryTerms']
            a = [word.lower() for word in wordpunct_tokenize(answer_list)]
            answer_length = len(a)
            interact = 0
            union = query_length + answer_length          
            for token in query_list:
                for atoken in a:
                    if token == atoken:
                        interact+=1

            probability = interact/union
            tup = (answer['target'], answer['queryTerms'], probability)
            probability_set.append(tup)

        max_probability = 0
        for p in probability_set:
            if p[2] > max_probability:
                max_probability = p[2]
                question_type = p[0]
        print max_probability
        return question_type


    def define_question_type(self, text, keywords):
        # Jaccard Coefficient mechanism
        # format
        sentence = self.change_format(text)
        s = text.lower()
        for key in keywords:
            if key[1] == 'title':
                s = s.replace(key[0], 'entity')
            elif key[1] == 'feature' or key[1] == 'goodrate' or key[1] =='badrate':
                s = s.replace(key[0], 'adjective')
            elif key[1] == 'price':
                s = s.replace(key[2], 'adjective')
            elif key[1] == 'postleft':
                s = s.replace(key[0], 'loc')
            elif key[1] == 'phone' or key[1] == 'speciality':
                s = s.replace(key[0], 'd')
        sentence = nltk.tokenize.sent_tokenize(s)

        for s in sentence:
            query_list = [word.lower() for word in wordpunct_tokenize(s)]
            query_length = len(query_list)

        # print query_list
        print query_list
        answers = []
        # Get data
        db = MySQLdb.connect(host='localhost', user='root',passwd='961127',db='django')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM question_type")
        results = cursor.fetchall()
        db.close()

        for row in results:
            r = {
            'target':row[0],
            'answerType':row[1],
            'queryTerms':row[2]
            }
            answers.append(r)

        return self.calculate_probability(answers, query_length, query_list)


