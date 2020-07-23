import TwitterAPI
import re
from datetime import datetime, timedelta

samples = ['@BarackObama',
           '@katyperry',
           '@justinbieber',
           '@rihanna',
           '@taylorswift13',
           '@Cristiano',
           '@ladygaga',
           '@TheEllenShow',
           '@elonmusk',
           '@ArianaGrande',
           '@realDonaldTrump',
           '@jtimberlake',
           '@KimKardashian',
           '@selenagomez',
           '@POTUS',
           '@britneyspears',
           '@cnnbrk',
           '@shakira',
           '@narendramodi',
           '@jimmyfallon']

emoji_pattern = re.compile("["
                           u"\U00002070-\U0010FFFF"  # Everything that is not Latin Alphabet

                           # U"\U00002700-\U000027BF"  # Dingbats 
                           # u"\U0001F600-\U0001F64F"  # emoticons
                           # u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           # u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           # u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)


def get_clean_tweets(tmln):
    clean_tweets = []
    for tweet in tmln:
        clean_tweet = re.sub(r'https://t.co/[a-zA-Z0-9./_\-]+', '', tweet.full_text)  # Remove links
        clean_tweet = clean_tweet.replace('\n', ' ')  # Remove new line symbols
        clean_tweet = emoji_pattern.sub(r' ', clean_tweet)  # Remove symbols (non-Latin Alphabet)
        clean_tweet = clean_tweet.strip()  # Strip extra whitespace
        if len(clean_tweet) > 0:  # Check that tweet wasn't just a link or emoji, has actual text
            clean_tweets.append(clean_tweet)
        else:
            pass

    return clean_tweets


if __name__ == "__main__":
    check_day = datetime.strftime(datetime.today() - timedelta(days=1), '%a %b %d')

    tweets = []

    for user in samples:
        timeline = TwitterAPI.get_tweets(user, check_day)

        if len(timeline) > 0:
            tweets.append(' '.join(get_clean_tweets(timeline)))
        else:
            continue

    str_tweets = ' '.join(tweets)

    # with open('/home/william/PycharmProjects/hegebot/text.txt', 'a') as file:
    #     file.write(str_tweets)
