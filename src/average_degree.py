#!/usr/bin/env python

#Program that calculates the average degree of hashtags
#Usage: python ./src/average_degree.py ./tweet_input/tweets.txt ./tweet_output/ft2.txt

import re
import datetime
import tweets_cleaned
import argparse
import sys


class TweetMetadata:
    def __init__(self, _hashtags, _timestamp):
        self.hashtags = _hashtags
        self.timestamp = _timestamp

    def __str__(self):
        return "Hashtags: " + ",".join(self.hashtags) + "\n" + "Timestamp: " + str(self.timestamp) + "\n"


def generate_graph(tweets_list):
    """
    :param tweets_list: tweets list
    :return: graph represented by adjecency list
    """
    graph = {}

    for tweet in tweets_list:
        if len(tweet.hashtags) < 2: continue

        for hashtag in tweet.hashtags:
            myindex = tweet.hashtags.index(hashtag)
            newlist = tweet.hashtags[:myindex] + tweet.hashtags[myindex + 1:]
            for item in newlist:
                graph.setdefault(hashtag, set()).add(item)
    return graph


def filter_tweets_sixty_seconds(tweets):
    """
    Get tweets within last 60 seconds
    :param tweets: list of tweets
    :return: subset of messages that fall within last 60 secs
    """
    if (len(tweets) == 0): return tweets
    lasttimestamp = tweets[-1].timestamp
    sixtysecondsbefore = lasttimestamp - datetime.timedelta(seconds=60)

    return filter(lambda x: x.timestamp > sixtysecondsbefore, tweets)

def calculate_average_degree(graph):
    """
    :param graph: graph of hashtags
    :return:  average degree rounded to 2 digits after decimal
    """
    degrees = 0.0
    # print(len(graph))
    for value in graph.values():
        degrees += len(value)
    return "{0:.2f}".format(degrees / len(graph))


def get_metadata(tweet_line):
    """
    Extract hashtags and timestamp from tweet
    :param tweet_line: cleaned twitter message
    :return: TweetMetadata object (list of hashtag, timestamp)
    """
    _hashtags = re.findall(r'#\w*', tweet_line)
    matchObj = re.search(r'\(timestamp:\s(.*?)\)', tweet_line, re.M | re.I)
    _timestamp = None
    if matchObj:
        twt_timestamp = matchObj.group(1)
        _timestamp = datetime.datetime.strptime(twt_timestamp, '%a %b %d %H:%M:%S +0000 %Y')

    return TweetMetadata(_hashtags, _timestamp)


def process_tweets(input_file_path, output_file_path):
    """
    :param input_file_path: Input filename containing twitter JSON messages
    :param output_file_path: Output file containing rolling average
    """
    tweets = []

    # Empty out the file first
    open(output_file_path, 'w').close()

    with open(input_file_path) as input_file:
        for line in input_file:
            # extract relevant, clean information from input line
            clean_text, created_timestamp, hasunicode = tweets_cleaned.clean_line(line)
            if clean_text:
                tweet = get_metadata(clean_text)
                if len(tweet.hashtags) < 2: continue
                #print tweet

                tweets.append(tweet)
                # filter according to time stamp
                tweets = filter_tweets_sixty_seconds(tweets)
                graph = generate_graph(tweets)
                with open(output_file_path, "a") as output_file:
                    output_file.write("{}\n".format(calculate_average_degree(graph)))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*")
    args = parser.parse_args()

    if len(args.files) != 2:
        print "Incorrect number of parameters. Exiting.."
        sys.exit()

    input_file_path = args.files[0]
    output_file_path = args.files[1]

    print "Calculating average_degree...\n"
    process_tweets(input_file_path, output_file_path)

    print "Completed...\n"
