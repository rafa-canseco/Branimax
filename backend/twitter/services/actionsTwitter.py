from twitter.instances.persons import person1, person2, person3, client, person4
from functions.openai_requests import generate_tweet,generate_response,generate_resume, generate_tweet,generate_tweet_url,generate_tweet_simple
from functions.querys_db import getPrompt


def get_tweet(person,id):
    response = person.get_tweet(id=id)
    tweetOrigin = response.data['text']
    return tweetOrigin

def likeTweet(person,tweetId):
    response = person.create_like(tweetId)
    print(response)

def response_tweet(idPerson,person,tweet_id,tweetOriginal,indicacion,hasthag):
    prompt = getPrompt(idPerson)
    response =generate_response(prompt,tweetOriginal,indicacion,hasthag)
    response_tweet = person.create_tweet(text=response, in_reply_to_tweet_id=tweet_id)
    tweet_response_id = response_tweet.data['id']
    return tweet_response_id

def response_simulated_tweet(idPerson,person,tweet_id,tweet_original,indicacion,hashtag):
    prompt = getPrompt(idPerson)
    response = generate_response(prompt,tweet_original,indicacion,hashtag)
    return response

def response_single_tweet(idPerson,person,topic,hashtag):
    prompt = getPrompt(idPerson)
    response = generate_tweet(prompt, topic, hashtag)
    tweet = person.create_tweet(text=response)
    print(tweet)
    tweet_id = tweet.data['id']
    print(tweet_id)
    return tweet_id

def response_single_tweet_url(idPerson,person,topic,hashtag,url):
    prompt = getPrompt(idPerson)
    response = generate_tweet_url(prompt, topic, hashtag,url)
    tweet = person.create_tweet(text=response)
    print(tweet)
    tweet_id = tweet.data['id']
    print(tweet_id)
    return tweet_id

def createCasualTweet(idPerson,person):
    prompt = getPrompt(idPerson)
    response = generate_tweet_simple(prompt)
    tweet = person.create_tweet(text=response)
    print(tweet)
    tweet_id = tweet.data['id']
    print(tweet_id)
    return tweet_id