import TwitterAPI
import re
from datetime import datetime

samples = ['@BarackObama',
           '@katyperry',
           '@justinbieber',
           '@rihanna',
           '@taylorswift13',
           '@Cristiano',
           '@ladygaga',
           '@TheEllenShow',
           '@YouTube',
           '@ArianaGrande',
           '@realDonaldTrump',
           '@jtimberlake',
           '@KimKardashian',
           '@selenagomez',
           '@Twitter',
           '@britneyspears',
           '@cnnbrk',
           '@shakira',
           '@narendramodi',
           '@jimmyfallon']


def get_clean_tweets(tmln):
    clean_tweets = []
    for tweet in tmln:
        clean_tweet = re.sub(r'https://t.co/[a-zA-Z0-9./_\-]+', '', tweet.full_text)
        clean_tweet = clean_tweet.replace('\n', ' ')
        if len(clean_tweet) > 0:
            clean_tweets.append(clean_tweet)
        else:
            pass

    return clean_tweets


if __name__ == "__main__":
    today = datetime.strftime(datetime.today(), '%a %b %d')
    timeline = TwitterAPI.get_tweets('@realDonaldTrump', today)
    tweets = get_clean_tweets(timeline)
    str_tweets = ' '.join(tweets)
    # TODO find out how to address emoji
    # with open('C:/Users/whege/Documents/hegebot/text.txt', 'a') as file:
    #     file.write(str_tweets)
