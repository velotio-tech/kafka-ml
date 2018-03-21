# import required libraries
from kafka import SimpleProducer, KafkaClient
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from twitter_config import consumer_key, consumer_secret, access_token, access_token_secret
import json

# Kafka settings
topic = b'twitter-stream'

# setting up Kafka producer
kafka = KafkaClient('localhost:9092')
producer = SimpleProducer(kafka)

class KafkaPusher(StreamListener):
    
    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data["text"]
        producer.send_messages(topic, tweet.encode('utf-8'))
        return True
    
    def on_error(self, status):
        print status

WORDS_TO_TRACK = ["Politics","Apple","Google","Microsoft","Bikes","Harley Davidson","Medicine"]

if __name__ == '__main__':
    l = KafkaPusher()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    while True:
        try:
            stream.filter(languages=["en"], track=WORDS_TO_TRACK)
        except:
            pass
