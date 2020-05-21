import requests
from bs4 import BeautifulSoup
import csv
import webbrowser
import io
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk import sent_tokenize, word_tokenize, pos_tag
from examplereplacer import AntonymReplacer
from statistics import mean
lemmatizer = WordNetLemmatizer()


# Sentiment Analysis

def penn_to_wn(tag):
    """
    Convert between the PennTreebank tags to simple Wordnet tags
    """
    if tag.startswith('J'):
        return wn.ADJ
    if tag.startswith('N'):
        return wn.NOUN
    if tag.startswith('R'):
        return wn.ADV
    if tag.startswith('V'):
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


# Scraper


def display(content, filename='output.html'):
    with open(filename, 'wb') as f:
        f.write(content)
        webbrowser.open(filename)


def get_soup(session, url, show=False):
    r = session.get(url)
    if show:
        display(r.content, 'temp.html')

    if r.status_code != 200:  # not OK
        print('[get_soup] status code:', r.status_code)
    else:
        return BeautifulSoup(r.text, 'html.parser')


def post_soup(session, url, params, show=False):
    '''Read HTML from server and convert to Soup'''

    r = session.post(url, data=params)

    if show:
        display(r.content, 'temp.html')

    if r.status_code != 200:  # not OK
        print('[post_soup] status code:', r.status_code)
    else:
        return BeautifulSoup(r.text, 'html.parser')


def scrape(count, url, lang='ALL'):
    # create session to keep all cookies (etc.) between requests
    session = requests.Session()

    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0',
    })
    items = parse(count, session, url + '?filterLang=' + lang)
    return items


def parse(count, session, url):
    '''Get number of reviews and start getting subpages with reviews'''

    print('\nParsing URL:', url)

    soup = get_soup(session, url)

    if not soup:
        print('[parse] no soup:', url)
        return

    num_reviews = soup.find(
        'span', class_='hotels-community-content-common-TabAboveHeader__tabCount--26Tct').text  # get text
    # print("num_reviews 1 is", num_reviews)
    # num_reviews = num_reviews[1:-1]
    # print("num_reviews 2 is", num_reviews)
    # num_reviews = num_reviews.replace(',', '')
    # print("num_reviews 3 is", num_reviews)
    num_reviews = int(num_reviews)  # convert text into integer
    print('\nTotal number of reviews to parse:', num_reviews)

    url_template = url.replace('.html', '-or{}.html', )
    # print('[parse] url_template:', url_template)

    items = []

    offset = 0

    while (True):
        subpage_url = url_template.format(offset)

        subpage_items = parse_reviews(count, session, subpage_url)
        if not subpage_items:
            break

        items += subpage_items

        if len(subpage_items) < 5:
            break

        offset += 5

    return items


def get_reviews_ids(soup):
    items = soup.find_all('div', attrs={'data-reviewid': True})

    if items:
        reviews_ids = [x.attrs['data-reviewid'] for x in items][::1]
        # print('[get_reviews_ids] data-reviewid:', reviews_ids)
        return reviews_ids


def get_more(session, reviews_ids):
    url = 'https://www.tripadvisor.com/OverlayWidgetAjax?Mode=EXPANDED_HOTEL_REVIEWS_RESP&metaReferer=Hotel_Review'

    payload = {
        # ie. "577882734,577547902,577300887",
        'reviews': ','.join(reviews_ids),
        # 'contextChoice': 'DETAIL_HR', # ???
        'widgetChoice': 'EXPANDED_HOTEL_REVIEW_HSX',  # ???
        'haveJses': 'earlyRequireDefine,amdearly,global_error,long_lived_global,apg-Hotel_Review,apg-Hotel_Review-in,bootstrap,desktop-rooms-guests-dust-en_US,responsive-calendar-templates-dust-en_US,taevents',
        'haveCsses': 'apg-Hotel_Review-in',
        'Action': 'install',
    }

    soup = post_soup(session, url, payload)

    return soup


l1 = []
l2 = []


def parse_reviews(count, session, url):
    '''Get all reviews from one page'''

    # print('[parse_reviews] url:', url)

    soup = get_soup(session, url)

    if not soup:
        print('[parse_reviews] no soup:', url)
        return

    hotel_name = soup.find('h1', id='HEADING').text

    reviews_ids = get_reviews_ids(soup)
    if not reviews_ids:
        return

    soup = get_more(session, reviews_ids)

    if not soup:
        print('[parse_reviews] no soup:', url)
        return

    items = []

    for idx, review in enumerate(soup.find_all('div', class_='reviewSelector')):

        badgets = review.find_all('span', class_='badgetext')
        if len(badgets) > 0:
            contributions = badgets[0].text
        else:
            contributions = '0'

        if len(badgets) > 1:
            helpful_vote = badgets[1].text
        else:
            helpful_vote = '0'
        user_loc = review.select_one('div.userLoc strong')
        if user_loc:
            user_loc = user_loc.text
        else:
            user_loc = ''

        bubble_rating = review.select_one('span.ui_bubble_rating')['class']
        bubble_rating = bubble_rating[1].split('_')[-1]

        item = {
            'review_body': review.find('p', class_='partial_entry').text,
        }

        items.append(item)
        # print('\n--- review ---\n')
        for key, val in item.items():
            # print(' ', key, ':', val)
            if count == 1:
                l1.append(val)

            elif count == 2:
                l2.append(val)
    return items


def write_in_csv(items, filename='results.csv',
                 headers=['hotel name', 'review title', 'review body',
                          'review date', 'contributions', 'helpful vote',
                          'user name', 'user location', 'rating'],
                 mode='w'):
    print('--- CSV ---')

    with io.open(filename, mode, encoding="utf-8") as csvfile:
        csv_file = csv.DictWriter(csvfile, headers)

        if mode == 'w':
            csv_file.writeheader()

        csv_file.writerows(items)


DB_COLUMN = 'review_body'
DB_COLUMN1 = 'review_date'

start_urls = [
    'https://www.tripadvisor.in/Hotel_Review-g297628-d10673745-Reviews-Hotel_Pent_House-Bengaluru_Bangalore_District_Karnataka.html',
    'https://www.tripadvisor.in/Hotel_Review-g297628-d13391641-Reviews-Octave_Plaza_Hotel-Bengaluru_Bangalore_District_Karnataka.html'
]

lang = 'en'

headers = [
    DB_COLUMN,
    DB_COLUMN1,
]

count = 0
name = []
for url in start_urls:
    count += 1
    # get all reviews for 'url' and 'lang'
    items = scrape(count, url, lang)

    if not items:
        print('No reviews')
    else:
        print("\nNo of accommodations to compare: ", count)
        # for d in items:
        #     for i in d:
        #         if i != "review_date":
        #             sentiment_scores(d[i], count)
        filename = url.split('Reviews-')[1][:-5] + '__' + lang
        # print('filename:', filename)
        # For generating CSV uncomment this
        name.append((url.split('Reviews-')[1][:-44]).replace('_', ' '))
        # write_in_csv(items, filename + '.csv', headers, mode='w')

s1 = []
s2 = []
print("\nLength of l1", len(l1))
print("\nLength of l2", len(l2))
for i in range(len(l1)):
    num = swn_polarity(l1[i])
    s1.append(num)
for i in range(len(l2)):
    num = swn_polarity(l2[i])
    s2.append(num)
m1 = mean(s1)
m2 = (mean(s2))

if m1 > m2:
    print('\n' + str(name[0]) + " is better than " + str(name[1]))
else:
    print('\n' + str(name[1]) + " is better than " + str(name[0]))
