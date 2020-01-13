import TwitterAPI
import re

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
tweet_dict = {}


def get_clean_tweets(user):
    clean_tweets = []
    timeline = TwitterAPI.get_tweets(user)
    for tweet in timeline:
        print(tweet.full_text)
        clean_tweet = re.sub(r':?\shttps://t.co/[a-zA-Z1-9./_\-]+\b', '', tweet.full_text)
        clean_tweet = clean_tweet.replace('\n', '')
        if len(clean_tweet) > 0:
            clean_tweets.append(clean_tweet)
        else:
            pass

    return clean_tweets


if __name__ == "__main__":
    test = get_clean_tweets('@BarackObama')

    # for sample in samples:
    #     tweet_dict[sample] = get_clean_tweets(sample)
