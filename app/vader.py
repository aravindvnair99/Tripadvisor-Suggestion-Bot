from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def sentiment_scores(sentence):

    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # oject gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)

    print("Overall sentiment dictionary is : ", sentiment_dict)
    print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")

    print("Sentence Overall Rated As", end=" ")

    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05:
        print("Positive")

    elif sentiment_dict['compound'] <= - 0.05:
        print("Negative")

    else:
        print("Neutral")


# Driver code
if __name__ == "__main__":

    # print("\n1st statement :")
    # sentence = "Geeks For Geeks is the best portal for \
    #     the computer science engineering students."

    # # function calling
    # sentiment_scores(sentence)

    # print("\n2nd Statement :")
    # sentence = "study is going on as usual"
    # sentiment_scores(sentence)
    filtered_sentence = []
    print("\n3rd Statement :")
    sentence = "Put some sentence here."
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(sentence)
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    filtered_sentence[0:] = [' '.join(filtered_sentence[0:])]
    print(filtered_sentence)
    sentiment_scores(filtered_sentence)
