from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk import sent_tokenize, word_tokenize, pos_tag
from examplereplacer import AntonymReplacer

lemmatizer = WordNetLemmatizer()


def penn_to_wn(tag):
    """
    Convert between the PennTreebank tags to simple Wordnet tags
    """
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    elif tag.startswith('V'):
        return wn.VERB
    return None


def swn_polarity(text):
    """
    Return a sentiment polarity: 0 = negative, 1 = positive
    """

    sentiment = 0.0
    tokens_count = 0
    b = ""
    if "not" in text:
        x = ""
        raw_sentences = sent_tokenize(text)
        for raw_sentence in raw_sentences:
            tagged_sentence = pos_tag(word_tokenize(raw_sentence))

            for word, tag in tagged_sentence:
                wn_tag = penn_to_wn(tag)
                if wn_tag in (wn.NOUN, wn.ADJ):
                    x = x + " " + word
                elif word == 'not':
                    x = x + " " + word
                else:
                    continue
        rep = AntonymReplacer()
        a = rep.negreplace(x)
        for i in range(len(a)):
            b = b + " " + str(a[i])
    if b == "":
        b = text
    print(b)
    raw_sentences = sent_tokenize(b)
    for raw_sentence in raw_sentences:
        tagged_sentence = pos_tag(word_tokenize(raw_sentence))

        for word, tag in tagged_sentence:
            wn_tag = penn_to_wn(tag)
            if wn_tag not in (wn.NOUN, wn.ADJ, wn.ADV):
                continue

            lemma = lemmatizer.lemmatize(word, pos=wn_tag)
            if not lemma:
                continue

            synsets = wn.synsets(lemma, pos=wn_tag)
            if not synsets:
                continue

            # Take the first sense, the most common
            synset = synsets[0]
            swn_synset = swn.senti_synset(synset.name())

            sentiment += swn_synset.pos_score() - swn_synset.neg_score()
            tokens_count += 1
    return sentiment


num = swn_polarity("movie is not at all clear")
print(num)
num1 = swn_polarity("movie is pretty good")
print(num1)
num2 = swn_polarity("This hotel has everything needed. We are from Australia and we loved our stay. Room was simple clean and we choose the partial ocean view room it was a great view. And pool was great. Free filtered water whenever you want and great location. Shops on the same street, park across the road and beach across the road. Tour buses stop out front. Sounds to good to be true. Staff were lovely. Canâ€™t say this about many hotels but this was a great stay for us. Our room view. ")
print(num2)
