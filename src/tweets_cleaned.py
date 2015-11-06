#!/usr/bin/env python

#Program that calculates the number of tweets cleaned
#Usage: python ./src/tweets_cleaned.py ./tweet_input/tweets.txt ./tweet_output/ft1.txt

# Imports
import json
import re
import argparse
import sys


def clean_line(line):
    """
    Extract relevant text from a twitter message and Clean it.

    :param line: Twitter JSON message as a single line
    :return: cleaned text of tweet,timestamp of tweet, hasUniCode - boolean to indicate if message has Unicode
    """
    hasUnicode = False

    # return if incorrect data
    if '{"limit":{"track":' in line:
        return None, None, False

    tweet_json = json.loads(line)
    # get created datetime of tweet
    created_timestamp = tweet_json["created_at"]

    # get text of tweet ; if unicode clean it
    text = tweet_json["text"]

    try:
        text.decode('ascii')
    except:
        hasUnicode = True
        clean_text = text.encode('ascii', 'ignore')
    else:
        clean_text = text

    # replace escaped characters
    clean_text = clean_text.replace('\\/', '/')
    clean_text = clean_text.replace('\\\\','\\')
    clean_text = clean_text.replace("\'", "'")
    clean_text = clean_text.replace("\\\"", "\"")
    clean_text = re.sub("\s+", " ", clean_text).strip()

    clean_text = "{} (timestamp: {})".format(clean_text, created_timestamp)

    return clean_text, created_timestamp, hasUnicode


def process_tweets_file(input_file_path, output_file_path):
    """
    :param input_file_path: Input filename containing twitter JSON messages
    :param output_file_path: Output file containing results
    """
    count_unicode = 0
    outputlines = []

    #read input file line by line
    with open(input_file_path) as input_file:
        for tweet in input_file:
            # Construct output line
            clean_text, created_timestamp, hasunicode = clean_line(tweet)
            if clean_text:
                if hasunicode: count_unicode += 1
                outputlines.append(clean_text)

    #construct file footer with unicode count
    output_file_footer = "{} tweets contained unicode".format(count_unicode)
    outputlines.append("\n%s" % output_file_footer)

    #Write results to output file
    with open(output_file_path, "w") as output_file:
        for item in outputlines:
            output_file.write("%s\n" % item)


if __name__ == '__main__':
    print "Starting tweets_cleaned ...\n"

    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*")
    args = parser.parse_args()

    if len(args.files) != 2:
        print "Incorrect number of parameters. Exiting.."
        sys.exit()

    input_file_path = args.files[0]
    output_file_path = args.files[1]
    #Process the input file containing Twitter JSON message, output results to output file
    process_tweets_file(input_file_path, output_file_path)

    print "Completed...\n"
