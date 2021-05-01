import tensorflow as tf
import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import numpy as np
import pandas as pd
import pickle
from flask import Flask, redirect, url_for, render_template, request
import tweepy
import sys
app = Flask(__name__)
import os
from sklearn import *
from collections import Counter
from langdetect import detect



a = []
l = 5
info = ""
num_comments = 0

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        info = request.form["twitter_id"]
        num_comments = request.form["number_of_comments_id"]
        username = str(info)

        maxreplies = int(num_comments)
        tweet_replies = []
       
        def tweetextraction(username,maxreplies):
            consumer_key = "nuVGJn0bEsYiKJ7mKAPTwkskK"
            consumer_secret = "XwrP0uU74FzgOE2p5X2EFkgLtrv4sXEvwOBl1FgmSR1gjOM5SX"
            access_token = "1284091258638462976-0aO8tuh7lhsWXtf6Jck2vV1twJzGE4"
            access_token_secret = "x7Ux4p4AwW7oZocVYhwTJZEYVlSUzo20EOW4WX4B1CyLw"
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth,wait_on_rate_limit=True)
            tweetwithreply = dict()
            i=0 
            for full_tweets in tweepy.Cursor(api.user_timeline,screen_name=username,timeout=999).items(1):
                tweet=full_tweets.text
            for replies in tweepy.Cursor(api.search,q='to:'+username,result_type='mixed',timeout=999).items(100):
                if hasattr(replies, 'in_reply_to_status_id_str'):
                    if (replies.in_reply_to_status_id_str==full_tweets.id_str and i<maxreplies):
                        strr=detect(replies.text)
                        if (strr=='en'):
                          i+=1
                          tweet_replies.append(replies.text)
                          #print(i)
            return tweet

        tweet = tweetextraction(username, maxreplies)
        model = tf.keras.models.load_model('model_file.pickle')
        with open('tokenizers.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)

        tweet_input = tweet_replies
        print(tweet_input)

        new_sequences = tokenizer.texts_to_sequences(tweet_input)
        new_padded = pad_sequences(new_sequences, padding='post', maxlen=1000)

        tweet1 = tweetextraction(username, maxreplies)
        model1 = tf.keras.models.load_model('model_ok.pickle')
        with open('tokenizerrr.pickle', 'rb') as handle:
            tokenizerrr = pickle.load(handle)

        tweet_input2 = tweet_replies
        print(tweet_input2)

        new_sequences1 = tokenizerrr.texts_to_sequences(tweet_input)
        new_padded1 = pad_sequences(new_sequences1, padding='post', maxlen=342)
        try:
            predictions = model.predict(new_padded)
            predictions2 = model.predict(new_padded1)
            output = list(map(lambda x,y: 'Rude' if (x + y)/2 > 0.5  else 'Not Rude', predictions,predictions2))
            a = list(map(list, zip(output, tweet_input)))
            print(a)
        
            return render_template("classification.html", content=a)
        except NameError as error:
            
            
            return render_template("hmya.html") 
        
        
        
    else:
        return render_template("bullying.html")


#return redirect(url_for("user", usr=a))
#@app.route("/<usr>")
#def user(usr):
    #return render_template("classification.html", content=a)


if __name__ == "__main__":
    app.run(debug=True)


