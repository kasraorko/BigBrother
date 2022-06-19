from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import os
import socket
import gzip

# # # # TWEET SHIPPER # # # #
class TweetShipper():
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def shipper(self, msg):
        self.msg = msg
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            bytemsg = bytes(self.msg, encoding='utf-8')
            s.sendall(bytemsg)


# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        pass

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = StdOutListener(fetched_tweets_filename)
        auth = OAuthHandler(str(os.environ['CONSUMER_KEY']), str(os.environ['CONSUMER_SECRET']))
        auth.set_access_token(str(os.environ['ACCESS_TOKEN']), str(os.environ['ACCESS_TOKEN_SECRET']))
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class StdOutListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            t = TweetShipper("172.16.78.71", 4015)
            t.shipper(data)
            with gzip.open(self.fetched_tweets_filename, 'ab') as tf:
                tf.write(data.encode('utf-8'))
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        try:
            print(status)
            t = TweetShipper("172.16.78.71", 4015)
            t.shipper(status)
            with gzip.open(self.fetched_tweets_filename, 'ab') as tf:
                tf.write(data.encode('utf-8'))
            return True
        except BaseException as e:
            print("Error on_status %s" % str(e))
        return True


if __name__ == '__main__':
    # Authenticate using config.py and connect to Twitter Streaming API.
    hash_tag_list = ["uber"] ## commas as OR space as AND
    fetched_tweets_filename = "/usr/src/app/tweets/tweets.gz"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
