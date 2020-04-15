# import SentimentIntensityAnalyzer class
# from vaderSentiment.vaderSentiment module.
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords

from nltk.tokenize import word_tokenize

# function to print sentiments
# of the sentence.


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
    sentence = "Hai Guys, we a group of 25 people stayed in this hotel on 27th Dec 2012. This is the WORST WORST WORST Ever Hotel I have ever seen in my entire lifetime. Please be aware it is not a Three star hotel and should be rated as ZERO STAR HOTEL. The Photos in their website might have been taken long time back while inaugurating the Hotel. Inside the Hotel is terrible. It is better to stay on platform rather than this Hotel. The Rooms are very bad, the mattresses are very very hard and nobody can sleep on them. Food in the restaurant is the worst I have ever tasted. Even dogs can not eat it. Since we are travelling with small kids, we requested them to provide some milk. The immediate answer is they don't have milk. After lot of requests, they have provided 1/2 litre diluted milk for Rs 150/-. They are Two lifts, among which one Lift is not working at all, and the other Lift is terrible, the doors get closed even during when people move in to it and you have to forcefully stop the doors with hands. We were scared with this Lift and used the staircases to reach our rooms located in 3rd floor along with heavy luggage. The Bathrooms are badly stinking. The Toilet Flush did not work. There was no hot water. Since, we had to catch a flight in the morning, we informed the hotel people in advance that we require Hot water by 4:30 A.M. None of our rooms got Hot water in the morning. The Staff told that they have already started the boiler, it takes 10 minutes. Even by 5:30 A.M, also we did not get the Hot water in the Taps. After lot of arguments, we got the Hot water by 5:45 A.M, but this time interestingly, we got extreme hot water with more than 100 degrees Celsius, and no cold water for mixing up to take the bath. Generally Hotels consist of both the Cold as well as Hot water Taps separately. But in this hotel it is not so. At any time you will get only one type of water either cold or hot. Finally, we could not take our bath, since we are already behind our schedule by 40 minutes. We worried a lot about reaching airport in time and catching our flight. This hotel didn't deserve the amount we paid. The Hotel people are biggest cheaters and they don't have any concern about the customers. Please avoid this WORST WORST WORST HOTEL. Thanks."
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(sentence)
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    filtered_sentence[0:] = [' '.join(filtered_sentence[0:])]
    print(filtered_sentence)
    sentiment_scores(filtered_sentence)
