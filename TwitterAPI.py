import twitter

user = '@hegebot'
user_id = 1216199305326927877

api = twitter.Api(consumer_key='A6qAY3a2FxtUHV1CGtHSv6GQy',
                  consumer_secret='6KKGPoD9t6hjrEFMSSFyHR0r2zR1qNqFQOM3YVkV956MbvNO2b',
                  access_token_key='1216199305326927877-6v39cFBjoee8ewssdEAE1EUu9ksRCp',
                  access_token_secret='qaLv8Fqp22mam5RcgPSWA1BxHys5FA2CZc33IopNW58JC',
                  tweet_mode='extended')


def send_tweet(tweet):
    tweet = api.PostUpdate(tweet)
    print(f"Sending tweet: '{tweet.text}'")


def get_tweets(u):
    return api.GetUserTimeline(screen_name=u, count=10, exclude_replies=False, include_rts=False)


def get_mentions():
    return api.GetMentions(trim_user=True, contributor_details=True)


def get_friends(u):
    return api.GetFriends(screen_name=u)


def get_followers(u):
    return api.GetFollowers(screen_name=u), api.GetFollowerIDs(screen_name=u)
