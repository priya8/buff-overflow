import pykafka
import json
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import cred

#TWITTER API CONFIGURATIONS
consumer_key = cred.CONSUMER_KEY
consumer_secret = cred.CONSUMER_SECRET
access_token = cred.ACCESS_TOKEN
access_secret = cred.ACCESS_TOKEN_SECRET

# TWITTER API AUTH
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


# Twitter Stream Listener
class KafkaPushListener(StreamListener):
    def __init__(self):
        # localhost:9092 = Default Zookeeper Producer Host and Port Adresses
        self.client = pykafka.KafkaClient("localhost:9092")

        # Get Producer that has topic name is Twitter
        self.producer = self.client.topics[bytes("twitter", "ascii")].get_producer()

    def on_data(self, data):
        # Producer produces data for consumer
        # Data comes from Twitter
        self.producer.produce(bytes(data, "ascii"))
        return True

    def on_error(self, status):
        print(status)
        return True


# Twitter Stream Config
twitter_stream = Stream(auth, KafkaPushListener())

# Produce Data that has COVID (Tweets)
twitter_stream.filter(track=['#COVID'])