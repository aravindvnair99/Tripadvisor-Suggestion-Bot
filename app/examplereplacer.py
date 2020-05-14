<<<<<<< HEAD
import re
=======
>>>>>>> b3f1054ff5f78639f335e07973a17f424ca69e5c
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize


class AntonymReplacer(object):
    def replace(self, word):
        ant = list()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                if lemma.antonyms():
                    ant.append(lemma.antonyms()[0].name())
        if len(ant) >= 1:
            return ant[0]
        else:
            return None

    def negreplace(self, string):
        i = 0
        sent = word_tokenize(string)
        len_sent = len(sent)
        words = []
        while i < len_sent:
            word = sent[i]
            if word == 'not' and i + 1 < len_sent:
                ant = self.replace(sent[i + 1])
                if ant:
                    words.append(ant)
                    i += 2
                    continue
            words.append(word)
            i += 1
        return words
