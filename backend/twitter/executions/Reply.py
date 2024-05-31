from twitter.services.actionsTwitter import response_tweet, get_tweet, response_simulated_tweet
import time
import random
from twitter.instances.persons import person1, person2, person3, person4, person5, person6, person7, person8, person9, person10, person11, person12, person13, person14, person15, person16, person17, person18, person19, person20, person21, person22, person23, person24, person25, person26, person27, person28, person29, person30, person31, person32, person33, person34, person35, person36, person37, person38, person39, person40, client
person_dict = {
    1: person1, 2: person2, 3: person3, 4: person4, 5: person5,
    6: person6, 7: person7, 8: person8, 9: person9, 10: person10,
    11: person11, 12: person12, 13: person13, 14: person14, 15: person15,
    16: person16, 17: person17, 18: person18, 19: person19, 20: person20,
    21: person21, 22: person22, 23: person23, 24: person24, 25: person25,
    26: person26, 27: person27, 28: person28, 29: person29, 30: person30,
    31: person31, 32: person32, 33: person33, 34: person34, 35: person35,
    36: person36, 37: person37, 38: person38, 39: person39, 40: person40
}


def respond_to_tweet(idTweetOriginal, indicacion, hashtag, botAssignments):
    tweetOriginal = get_tweet(client, idTweetOriginal)


    for assignment in botAssignments:
        idPerson = assignment.profileId
        num_bots = assignment.botCount
        for i in range(num_bots):
            try:
                person = person_dict[idPerson]
                response_tweet(idPerson, person, idTweetOriginal, tweetOriginal, indicacion, hashtag)
            except KeyError:
                print(f"Error: No se encontró la instancia de person{idPerson}")
            except Exception as e:
                print(f"Error al responder al tweet para person{idPerson}: {str(e)}")
            sleep_time = random.randint(1, 5)
            time.sleep(sleep_time)


def single_response_preview(idTweetOriginal,idPerson,indicacion,hashtag):

    tweetOriginal = get_tweet(client,idTweetOriginal)
    print(tweetOriginal)
    tweet = response_simulated_tweet(idPerson,person1,idTweetOriginal,tweetOriginal,indicacion,hashtag)
    return tweet