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


def get_links(tweet):
    links = []
    urls = tweet.urls
    media_urls = tweet.media
    for url in urls:
        links.append(url.url)
    if media_urls is not None:
        for mu in media_urls:
            links.append(mu.url)
    return links


def get_clean_tweets(user):
    timeline = TwitterAPI.get_tweets(user)
    clean_tweets = []
    for tweet in timeline:
        links = get_links(tweet)
        if len(links) > 0:
            for link in links:
                clean_tweets.append(tweet.full_text.replace(link, ''))
        else:
            clean_tweets.append(tweet.full_text)

    return clean_tweets


if __name__ == "__main__":
    for sample in samples:
        tweet_dict[sample] = get_clean_tweets(sample)
