# -*- coding: utf-8 -*-
from __future__ import division
import string
from itertools import groupby
import nltk
from nltk.tokenize import wordpunct_tokenize
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


    def get_keywords(self, text):
        sentence = nltk.tokenize.sent_tokenize(text)
        for s in sentence:
            parameter = self._generate_phrases(s)
            if type(parameter)==list:
                phrase_list = parameter[1]
                entity = parameter[0]
            else:
                phrase_list = parameter
        keywords = []
        for phrase in phrase_list:
            keywords.append(' '.join(phrase))
        keywords = [entity if x == 'entity' else x for x in keywords]

        return keywords

    def find_entity(self, sentence):
        # identify the entity in a sentence
        db = MySQLdb.connect(host='localhost', user='root',passwd='961127',db='django')
        cursor = db.cursor()
        cursor.execute("SELECT title FROM Restaurants_data GROUP BY title")
        results = cursor.fetchall()
        db.close()
        title_list = []
        potential_entities = []
        # Delete ambiguous word
        sentence = sentence.replace('the','')
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
        else:
            sentence = nltk.tokenize.sent_tokenize(text)
        return sentence

    def _generate_phrases(self, sentence):
        phrase_list = set()
        potential_entities = self.find_entity(sentence)
        
        sentence = self.change_format(sentence)
        for s in sentence:
            word_list = [word.lower() for word in wordpunct_tokenize(s)]

        # The longest one will be identified to a entity
        if potential_entities:
            entity = max(potential_entities, key = len)
            s = sentence.lower().replace(entity, 'entity')
            word_list = wordpunct_tokenize(s)
        tagged = pos_tag(word_list)
        # Delete verb in the query
        for w, t in zip(word_list,tagged):
            if t[1] in ['VB', 'VBG', 'VBD','VBN','VBP','VBZ'] or t[0] == 'list':
                word_list.remove(w)

        phrase_list.update(self.get_phrases(word_list))

        if 'entity' in dir():
            parameter = [entity, phrase_list]
            return parameter
        else:
            return phrase_list
   
    def get_phrases(self, word_list):
        phrase_list = []
        for group in groupby(word_list, lambda x: x in self.to_ignore):
            if not group[0]:
                l = list(group[1])
                tagged = pos_tag(l)
                # seperate adjective words
                for w, t in zip(l, tagged):
                    if t[1] in ['JJ','JJR','JJS','RBS','RB','RBR'] or  not (t[0].find('ese') == -1):
                        l.remove(w)
                        adjective = (t[0], )
                        phrase_list.append(adjective)
                if l != []:
                    phrase_list.append(tuple(l))
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
            print tup
            probability_set.append(tup)

        max_probability = 0
        for p in probability_set:
            if p[2] > max_probability:
                max_probability = p[2]
                question_type = p[0]
        print(max_probability)
        print(question_type)


    def define_question_type(self, text):
        # Jaccard Coefficient mechanism
        potential_entities = self.find_entity(text)
        # format
        sentence = self.change_format(text)
        print sentence

        if potential_entities:
            entity = max(potential_entities, key = len)
            s = text.lower().replace(entity, 'entity')
            sentence = nltk.tokenize.sent_tokenize(s)

        for s in sentence:
            query_list = [word.lower() for word in wordpunct_tokenize(s)]
            query_length = len(query_list)

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

        self.calculate_probability(answers, query_length, query_list)


