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
            phrase_list = self._generate_phrases(s)

        keywords = []
        for phrase in phrase_list:
            keywords.append(' '.join(phrase))

        return keywords

    def _generate_phrases(self, sentence):
        phrase_list = set()
        word_list = [word.lower() for word in wordpunct_tokenize(sentence)]

        print word_list
        tagged = pos_tag(word_list)

        # Delete verb in the query
        for w, t in zip(word_list,tagged):
            if t[1] == 'VB' or t[0] == 'list':
                word_list.remove(w)

        phrase_list.update(self.get_phrases(word_list))
        return phrase_list
   
    def get_phrases(self, word_list):
        phrase_list = []
        for group in groupby(word_list, lambda x: x in self.to_ignore):
            if not group[0]:
                l = list(group[1])
                tagged = pos_tag(l)
                # seperate adjective words
                for w, t in zip(l, tagged):
                    print w, ':', t[1]
                    if t[1] in ['JJ','JJR','JJS','RBS','RB', 'RBR'] or  not(t[0].find('ese') == -1):
                        l.remove(w)
                        adjective = (t[0], )
                        print adjective
                        phrase_list.append(adjective)
                if l != []:
                    phrase_list.append(tuple(l))
        return phrase_list

    def define_question_type(self, text):
        # Jaccard Coefficient mechanism
        sentence = nltk.tokenize.sent_tokenize(text)
        for s in sentence:
            query_list = [word.lower() for word in wordpunct_tokenize(s)]
            query_length = len(query_list)

        answers = []
        db = MySQLdb.connect(host='localhost', user='root',passwd='961127',db='django')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM question_type")
        results = cursor.fetchall()
        for row in results:
            r = {
            'target':row[0],
            'answerType':row[1],
            'queryTerms':row[2]
            }
            answers.append(r)

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
        print(max_probability)
        print(question_type)
        db.close()
