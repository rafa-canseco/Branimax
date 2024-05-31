import os
from dotenv import load_dotenv
load_dotenv()
from telegram import Bot
import tweepy

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_CHAT_ID_RAFA =os.getenv("TELEGRAM_CHAT_ID_RAFA")
bot = Bot(token=TELEGRAM_TOKEN)

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY_ADMIN")
TWITTER_API_SECRET_KEY = os.getenv("TWITTER_API_SECRET_KEY_ADMIN")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN_ADMIN")
TWITTER_ACCESS_TOKEN_SECRET =os.getenv("TWITTER_ACCESS_TOKEN_SECRET_ADMIN")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN_ADMIN")

TWITTER_API_KEY_1 = os.getenv("TWITTER_API_KEY_P1")
TWITTER_API_SECRET_KEY_1 = os.getenv("TWITTER_API_SECRET_KEY_P1")
TWITTER_ACCESS_TOKEN_1 = os.getenv("TWITTER_ACCESS_TOKEN_P1")
TWITTER_ACCESS_TOKEN_SECRET_1 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P1")
TWITTER_BEARER_TOKEN_1 = os.getenv("TWITTER_BEARER_TOKEN_P1")

TWITTER_API_KEY_2 = os.getenv("TWITTER_API_KEY_P2")
TWITTER_API_SECRET_KEY_2 = os.getenv("TWITTER_API_SECRET_KEY_P2")
TWITTER_ACCESS_TOKEN_2 = os.getenv("TWITTER_ACCESS_TOKEN_P2")
TWITTER_ACCESS_TOKEN_SECRET_2 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P2")
TWITTER_BEARER_TOKEN_2 = os.getenv("TWITTER_BEARER_TOKEN_P2")

TWITTER_API_KEY_3 = os.getenv("TWITTER_API_KEY_P3")
TWITTER_API_SECRET_KEY_3 = os.getenv("TWITTER_API_SECRET_KEY_P3")
TWITTER_ACCESS_TOKEN_3 = os.getenv("TWITTER_ACCESS_TOKEN_P3")
TWITTER_ACCESS_TOKEN_SECRET_3 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P3")
TWITTER_BEARER_TOKEN_3 = os.getenv("TWITTER_BEARER_TOKEN_P3")

TWITTER_API_KEY_4 = os.getenv("TWITTER_API_KEY_P4")
TWITTER_API_SECRET_KEY_4 = os.getenv("TWITTER_API_SECRET_KEY_P4")
TWITTER_ACCESS_TOKEN_4 = os.getenv("TWITTER_ACCESS_TOKEN_P4")
TWITTER_ACCESS_TOKEN_SECRET_4 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P4")
TWITTER_BEARER_TOKEN_4 = os.getenv("TWITTER_BEARER_TOKEN_P4")

TWITTER_API_KEY_5 = os.getenv("TWITTER_API_KEY_P5")
TWITTER_API_SECRET_KEY_5 = os.getenv("TWITTER_API_SECRET_KEY_P5")
TWITTER_ACCESS_TOKEN_5 = os.getenv("TWITTER_ACCESS_TOKEN_P5")
TWITTER_ACCESS_TOKEN_SECRET_5 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P5")
TWITTER_BEARER_TOKEN_5 = os.getenv("TWITTER_BEARER_TOKEN_P5")

TWITTER_API_KEY_6 = os.getenv("TWITTER_API_KEY_P6")
TWITTER_API_SECRET_KEY_6 = os.getenv("TWITTER_API_SECRET_KEY_P6")
TWITTER_ACCESS_TOKEN_6 = os.getenv("TWITTER_ACCESS_TOKEN_P6")
TWITTER_ACCESS_TOKEN_SECRET_6 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P6")
TWITTER_BEARER_TOKEN_6 = os.getenv("TWITTER_BEARER_TOKEN_P6")

TWITTER_API_KEY_7 = os.getenv("TWITTER_API_KEY_P7")
TWITTER_API_SECRET_KEY_7 = os.getenv("TWITTER_API_SECRET_KEY_P7")
TWITTER_ACCESS_TOKEN_7 = os.getenv("TWITTER_ACCESS_TOKEN_P7")
TWITTER_ACCESS_TOKEN_SECRET_7 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P7")
TWITTER_BEARER_TOKEN_7 = os.getenv("TWITTER_BEARER_TOKEN_P7")

TWITTER_API_KEY_8 = os.getenv("TWITTER_API_KEY_P8")
TWITTER_API_SECRET_KEY_8 = os.getenv("TWITTER_API_SECRET_KEY_P8")
TWITTER_ACCESS_TOKEN_8 = os.getenv("TWITTER_ACCESS_TOKEN_P8")
TWITTER_ACCESS_TOKEN_SECRET_8 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P8")
TWITTER_BEARER_TOKEN_8 = os.getenv("TWITTER_BEARER_TOKEN_P8")

TWITTER_API_KEY_9 = os.getenv("TWITTER_API_KEY_P9")
TWITTER_API_SECRET_KEY_9 = os.getenv("TWITTER_API_SECRET_KEY_P9")
TWITTER_ACCESS_TOKEN_9 = os.getenv("TWITTER_ACCESS_TOKEN_P9")
TWITTER_ACCESS_TOKEN_SECRET_9 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P9")
TWITTER_BEARER_TOKEN_9 = os.getenv("TWITTER_BEARER_TOKEN_P9")

TWITTER_API_KEY_10 = os.getenv("TWITTER_API_KEY_P10")
TWITTER_API_SECRET_KEY_10 = os.getenv("TWITTER_API_SECRET_KEY_P10")
TWITTER_ACCESS_TOKEN_10 = os.getenv("TWITTER_ACCESS_TOKEN_P10")
TWITTER_ACCESS_TOKEN_SECRET_10 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P10")
TWITTER_BEARER_TOKEN_10 = os.getenv("TWITTER_BEARER_TOKEN_P10")

TWITTER_API_KEY_11 = os.getenv("TWITTER_API_KEY_P11")
TWITTER_API_SECRET_KEY_11 = os.getenv("TWITTER_API_SECRET_KEY_P11")
TWITTER_ACCESS_TOKEN_11 = os.getenv("TWITTER_ACCESS_TOKEN_P11")
TWITTER_ACCESS_TOKEN_SECRET_11 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P11")
TWITTER_BEARER_TOKEN_11 = os.getenv("TWITTER_BEARER_TOKEN_P11")

TWITTER_API_KEY_12 = os.getenv("TWITTER_API_KEY_P12")
TWITTER_API_SECRET_KEY_12 = os.getenv("TWITTER_API_SECRET_KEY_P12")
TWITTER_ACCESS_TOKEN_12 = os.getenv("TWITTER_ACCESS_TOKEN_P12")
TWITTER_ACCESS_TOKEN_SECRET_12 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P12")
TWITTER_BEARER_TOKEN_12 = os.getenv("TWITTER_BEARER_TOKEN_P12")

TWITTER_API_KEY_13 = os.getenv("TWITTER_API_KEY_P13")
TWITTER_API_SECRET_KEY_13 = os.getenv("TWITTER_API_SECRET_KEY_P13")
TWITTER_ACCESS_TOKEN_13 = os.getenv("TWITTER_ACCESS_TOKEN_P13")
TWITTER_ACCESS_TOKEN_SECRET_13 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P13")
TWITTER_BEARER_TOKEN_13 = os.getenv("TWITTER_BEARER_TOKEN_P13")

TWITTER_API_KEY_14 = os.getenv("TWITTER_API_KEY_P14")
TWITTER_API_SECRET_KEY_14 = os.getenv("TWITTER_API_SECRET_KEY_P14")
TWITTER_ACCESS_TOKEN_14 = os.getenv("TWITTER_ACCESS_TOKEN_P14")
TWITTER_ACCESS_TOKEN_SECRET_14 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P14")
TWITTER_BEARER_TOKEN_14 = os.getenv("TWITTER_BEARER_TOKEN_P14")

TWITTER_API_KEY_15 = os.getenv("TWITTER_API_KEY_P15")
TWITTER_API_SECRET_KEY_15 = os.getenv("TWITTER_API_SECRET_KEY_P15")
TWITTER_ACCESS_TOKEN_15 = os.getenv("TWITTER_ACCESS_TOKEN_P15")
TWITTER_ACCESS_TOKEN_SECRET_15 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P15")
TWITTER_BEARER_TOKEN_15 = os.getenv("TWITTER_BEARER_TOKEN_P15")

TWITTER_API_KEY_16 = os.getenv("TWITTER_API_KEY_P16")
TWITTER_API_SECRET_KEY_16 = os.getenv("TWITTER_API_SECRET_KEY_P16")
TWITTER_ACCESS_TOKEN_16 = os.getenv("TWITTER_ACCESS_TOKEN_P16")
TWITTER_ACCESS_TOKEN_SECRET_16 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P16")
TWITTER_BEARER_TOKEN_16 = os.getenv("TWITTER_BEARER_TOKEN_P16")

TWITTER_API_KEY_17 = os.getenv("TWITTER_API_KEY_P17")
TWITTER_API_SECRET_KEY_17 = os.getenv("TWITTER_API_SECRET_KEY_P17")
TWITTER_ACCESS_TOKEN_17 = os.getenv("TWITTER_ACCESS_TOKEN_P17")
TWITTER_ACCESS_TOKEN_SECRET_17 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P17")
TWITTER_BEARER_TOKEN_17 = os.getenv("TWITTER_BEARER_TOKEN_P17")

TWITTER_API_KEY_18 = os.getenv("TWITTER_API_KEY_P18")
TWITTER_API_SECRET_KEY_18 = os.getenv("TWITTER_API_SECRET_KEY_P18")
TWITTER_ACCESS_TOKEN_18 = os.getenv("TWITTER_ACCESS_TOKEN_P18")
TWITTER_ACCESS_TOKEN_SECRET_18 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P18")
TWITTER_BEARER_TOKEN_18 = os.getenv("TWITTER_BEARER_TOKEN_P18")

TWITTER_API_KEY_19 = os.getenv("TWITTER_API_KEY_P19")
TWITTER_API_SECRET_KEY_19 = os.getenv("TWITTER_API_SECRET_KEY_P19")
TWITTER_ACCESS_TOKEN_19 = os.getenv("TWITTER_ACCESS_TOKEN_P19")
TWITTER_ACCESS_TOKEN_SECRET_19 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P19")
TWITTER_BEARER_TOKEN_19 = os.getenv("TWITTER_BEARER_TOKEN_P19")

TWITTER_API_KEY_20 = os.getenv("TWITTER_API_KEY_P20")
TWITTER_API_SECRET_KEY_20 = os.getenv("TWITTER_API_SECRET_KEY_P20")
TWITTER_ACCESS_TOKEN_20 = os.getenv("TWITTER_ACCESS_TOKEN_P20")
TWITTER_ACCESS_TOKEN_SECRET_20 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P20")
TWITTER_BEARER_TOKEN_20 = os.getenv("TWITTER_BEARER_TOKEN_P20")

TWITTER_API_KEY_21 = os.getenv("TWITTER_API_KEY_P21")
TWITTER_API_SECRET_KEY_21 = os.getenv("TWITTER_API_SECRET_KEY_P21")
TWITTER_ACCESS_TOKEN_21 = os.getenv("TWITTER_ACCESS_TOKEN_P21")
TWITTER_ACCESS_TOKEN_SECRET_21 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P21")
TWITTER_BEARER_TOKEN_21 = os.getenv("TWITTER_BEARER_TOKEN_P21")

TWITTER_API_KEY_22 = os.getenv("TWITTER_API_KEY_P22")
TWITTER_API_SECRET_KEY_22 = os.getenv("TWITTER_API_SECRET_KEY_P22")
TWITTER_ACCESS_TOKEN_22 = os.getenv("TWITTER_ACCESS_TOKEN_P22")
TWITTER_ACCESS_TOKEN_SECRET_22 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P22")
TWITTER_BEARER_TOKEN_22 = os.getenv("TWITTER_BEARER_TOKEN_P22")

TWITTER_API_KEY_23 = os.getenv("TWITTER_API_KEY_P23")
TWITTER_API_SECRET_KEY_23 = os.getenv("TWITTER_API_SECRET_KEY_P23")
TWITTER_ACCESS_TOKEN_23 = os.getenv("TWITTER_ACCESS_TOKEN_P23")
TWITTER_ACCESS_TOKEN_SECRET_23 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P23")
TWITTER_BEARER_TOKEN_23 = os.getenv("TWITTER_BEARER_TOKEN_P23")

TWITTER_API_KEY_24 = os.getenv("TWITTER_API_KEY_P24")
TWITTER_API_SECRET_KEY_24 = os.getenv("TWITTER_API_SECRET_KEY_P24")
TWITTER_ACCESS_TOKEN_24 = os.getenv("TWITTER_ACCESS_TOKEN_P24")
TWITTER_ACCESS_TOKEN_SECRET_24 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P24")
TWITTER_BEARER_TOKEN_24 = os.getenv("TWITTER_BEARER_TOKEN_P24")

TWITTER_API_KEY_25 = os.getenv("TWITTER_API_KEY_P25")
TWITTER_API_SECRET_KEY_25 = os.getenv("TWITTER_API_SECRET_KEY_P25")
TWITTER_ACCESS_TOKEN_25 = os.getenv("TWITTER_ACCESS_TOKEN_P25")
TWITTER_ACCESS_TOKEN_SECRET_25 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P25")
TWITTER_BEARER_TOKEN_25 = os.getenv("TWITTER_BEARER_TOKEN_P25")

TWITTER_API_KEY_26 = os.getenv("TWITTER_API_KEY_P26")
TWITTER_API_SECRET_KEY_26 = os.getenv("TWITTER_API_SECRET_KEY_P26")
TWITTER_ACCESS_TOKEN_26 = os.getenv("TWITTER_ACCESS_TOKEN_P26")
TWITTER_ACCESS_TOKEN_SECRET_26 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P26")
TWITTER_BEARER_TOKEN_26 = os.getenv("TWITTER_BEARER_TOKEN_P26")

TWITTER_API_KEY_27 = os.getenv("TWITTER_API_KEY_P27")
TWITTER_API_SECRET_KEY_27 = os.getenv("TWITTER_API_SECRET_KEY_P27")
TWITTER_ACCESS_TOKEN_27 = os.getenv("TWITTER_ACCESS_TOKEN_P27")
TWITTER_ACCESS_TOKEN_SECRET_27 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P27")
TWITTER_BEARER_TOKEN_27 = os.getenv("TWITTER_BEARER_TOKEN_P27")

TWITTER_API_KEY_28 = os.getenv("TWITTER_API_KEY_P28")
TWITTER_API_SECRET_KEY_28 = os.getenv("TWITTER_API_SECRET_KEY_P28")
TWITTER_ACCESS_TOKEN_28 = os.getenv("TWITTER_ACCESS_TOKEN_P28")
TWITTER_ACCESS_TOKEN_SECRET_28 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P28")
TWITTER_BEARER_TOKEN_28 = os.getenv("TWITTER_BEARER_TOKEN_P28")

TWITTER_API_KEY_29 = os.getenv("TWITTER_API_KEY_P29")
TWITTER_API_SECRET_KEY_29 = os.getenv("TWITTER_API_SECRET_KEY_P29")
TWITTER_ACCESS_TOKEN_29 = os.getenv("TWITTER_ACCESS_TOKEN_P29")
TWITTER_ACCESS_TOKEN_SECRET_29 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P29")
TWITTER_BEARER_TOKEN_29 = os.getenv("TWITTER_BEARER_TOKEN_P29")

TWITTER_API_KEY_30 = os.getenv("TWITTER_API_KEY_P30")
TWITTER_API_SECRET_KEY_30 = os.getenv("TWITTER_API_SECRET_KEY_P30")
TWITTER_ACCESS_TOKEN_30 = os.getenv("TWITTER_ACCESS_TOKEN_P30")
TWITTER_ACCESS_TOKEN_SECRET_30 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P30")
TWITTER_BEARER_TOKEN_30 = os.getenv("TWITTER_BEARER_TOKEN_P30")

TWITTER_API_KEY_31 = os.getenv("TWITTER_API_KEY_P31")
TWITTER_API_SECRET_KEY_31 = os.getenv("TWITTER_API_SECRET_KEY_P31")
TWITTER_ACCESS_TOKEN_31 = os.getenv("TWITTER_ACCESS_TOKEN_P31")
TWITTER_ACCESS_TOKEN_SECRET_31 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P31")
TWITTER_BEARER_TOKEN_31 = os.getenv("TWITTER_BEARER_TOKEN_P31")

TWITTER_API_KEY_32 = os.getenv("TWITTER_API_KEY_P32")
TWITTER_API_SECRET_KEY_32 = os.getenv("TWITTER_API_SECRET_KEY_P32")
TWITTER_ACCESS_TOKEN_32 = os.getenv("TWITTER_ACCESS_TOKEN_P32")
TWITTER_ACCESS_TOKEN_SECRET_32 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P32")
TWITTER_BEARER_TOKEN_32 = os.getenv("TWITTER_BEARER_TOKEN_P32")

TWITTER_API_KEY_33 = os.getenv("TWITTER_API_KEY_P33")
TWITTER_API_SECRET_KEY_33 = os.getenv("TWITTER_API_SECRET_KEY_P33")
TWITTER_ACCESS_TOKEN_33 = os.getenv("TWITTER_ACCESS_TOKEN_P33")
TWITTER_ACCESS_TOKEN_SECRET_33 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P33")
TWITTER_BEARER_TOKEN_33 = os.getenv("TWITTER_BEARER_TOKEN_P33")

TWITTER_API_KEY_34 = os.getenv("TWITTER_API_KEY_P34")
TWITTER_API_SECRET_KEY_34 = os.getenv("TWITTER_API_SECRET_KEY_P34")
TWITTER_ACCESS_TOKEN_34 = os.getenv("TWITTER_ACCESS_TOKEN_P34")
TWITTER_ACCESS_TOKEN_SECRET_34 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P34")
TWITTER_BEARER_TOKEN_34 = os.getenv("TWITTER_BEARER_TOKEN_P34")

TWITTER_API_KEY_35 = os.getenv("TWITTER_API_KEY_P35")
TWITTER_API_SECRET_KEY_35 = os.getenv("TWITTER_API_SECRET_KEY_P35")
TWITTER_ACCESS_TOKEN_35 = os.getenv("TWITTER_ACCESS_TOKEN_P35")
TWITTER_ACCESS_TOKEN_SECRET_35 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P35")
TWITTER_BEARER_TOKEN_35 = os.getenv("TWITTER_BEARER_TOKEN_P35")

TWITTER_API_KEY_36 = os.getenv("TWITTER_API_KEY_P36")
TWITTER_API_SECRET_KEY_36 = os.getenv("TWITTER_API_SECRET_KEY_P36")
TWITTER_ACCESS_TOKEN_36 = os.getenv("TWITTER_ACCESS_TOKEN_P36")
TWITTER_ACCESS_TOKEN_SECRET_36 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P36")
TWITTER_BEARER_TOKEN_36 = os.getenv("TWITTER_BEARER_TOKEN_P36")

TWITTER_API_KEY_37 = os.getenv("TWITTER_API_KEY_P37")
TWITTER_API_SECRET_KEY_37 = os.getenv("TWITTER_API_SECRET_KEY_P37")
TWITTER_ACCESS_TOKEN_37 = os.getenv("TWITTER_ACCESS_TOKEN_P37")
TWITTER_ACCESS_TOKEN_SECRET_37 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P37")
TWITTER_BEARER_TOKEN_37 = os.getenv("TWITTER_BEARER_TOKEN_P37")

TWITTER_API_KEY_38 = os.getenv("TWITTER_API_KEY_P38")
TWITTER_API_SECRET_KEY_38 = os.getenv("TWITTER_API_SECRET_KEY_P38")
TWITTER_ACCESS_TOKEN_38 = os.getenv("TWITTER_ACCESS_TOKEN_P38")
TWITTER_ACCESS_TOKEN_SECRET_38 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P38")
TWITTER_BEARER_TOKEN_38 = os.getenv("TWITTER_BEARER_TOKEN_P38")

TWITTER_API_KEY_39 = os.getenv("TWITTER_API_KEY_P39")
TWITTER_API_SECRET_KEY_39 = os.getenv("TWITTER_API_SECRET_KEY_P39")
TWITTER_ACCESS_TOKEN_39 = os.getenv("TWITTER_ACCESS_TOKEN_P39")
TWITTER_ACCESS_TOKEN_SECRET_39 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P39")
TWITTER_BEARER_TOKEN_39 = os.getenv("TWITTER_BEARER_TOKEN_P39")

TWITTER_API_KEY_40 = os.getenv("TWITTER_API_KEY_P40")
TWITTER_API_SECRET_KEY_40 = os.getenv("TWITTER_API_SECRET_KEY_P40")
TWITTER_ACCESS_TOKEN_40 = os.getenv("TWITTER_ACCESS_TOKEN_P40")
TWITTER_ACCESS_TOKEN_SECRET_40 = os.getenv("TWITTER_ACCESS_TOKEN_SECRET_P40")
TWITTER_BEARER_TOKEN_40 = os.getenv("TWITTER_BEARER_TOKEN_P40")

client  = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN,
                                         consumer_key=TWITTER_API_KEY,
                                         consumer_secret=TWITTER_API_SECRET_KEY,
                                         access_token=TWITTER_ACCESS_TOKEN,
                                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
                                         wait_on_rate_limit=True)

person1  = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_1,
                                         consumer_key=TWITTER_API_KEY_1,
                                         consumer_secret=TWITTER_API_SECRET_KEY_1,
                                         access_token=TWITTER_ACCESS_TOKEN_1,
                                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_1,
                                         wait_on_rate_limit=True)

person2  = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_2,
                                         consumer_key=TWITTER_API_KEY_2,
                                         consumer_secret=TWITTER_API_SECRET_KEY_2,
                                         access_token=TWITTER_ACCESS_TOKEN_2,
                                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_2,
                                         wait_on_rate_limit=True)

person3  = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_3,
                                         consumer_key=TWITTER_API_KEY_3,
                                         consumer_secret=TWITTER_API_SECRET_KEY_3,
                                         access_token=TWITTER_ACCESS_TOKEN_3,
                                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_3,
                                         wait_on_rate_limit=True)

person4 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_4,
                        consumer_key=TWITTER_API_KEY_4,
                        consumer_secret=TWITTER_API_SECRET_KEY_4,
                        access_token=TWITTER_ACCESS_TOKEN_4,
                        access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_4,
                        wait_on_rate_limit=True)

person5 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_5,
                        consumer_key=TWITTER_API_KEY_5,
                        consumer_secret=TWITTER_API_SECRET_KEY_5,
                        access_token=TWITTER_ACCESS_TOKEN_5,
                        access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_5,
                        wait_on_rate_limit=True)

person6 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_6,
                        consumer_key=TWITTER_API_KEY_6,
                        consumer_secret=TWITTER_API_SECRET_KEY_6,
                        access_token=TWITTER_ACCESS_TOKEN_6,
                        access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_6,
                        wait_on_rate_limit=True)

person7 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_7,
                        consumer_key=TWITTER_API_KEY_7,
                        consumer_secret=TWITTER_API_SECRET_KEY_7,
                        access_token=TWITTER_ACCESS_TOKEN_7,
                        access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_7,
                        wait_on_rate_limit=True)

person8 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_8,
                        consumer_key=TWITTER_API_KEY_8,
                        consumer_secret=TWITTER_API_SECRET_KEY_8,
                        access_token=TWITTER_ACCESS_TOKEN_8,
                        access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_8,
                        wait_on_rate_limit=True)

person9 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_9,
                        consumer_key=TWITTER_API_KEY_9,
                        consumer_secret=TWITTER_API_SECRET_KEY_9,
                        access_token=TWITTER_ACCESS_TOKEN_9,
                        access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_9,
                        wait_on_rate_limit=True)

person10 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_10,
                         consumer_key=TWITTER_API_KEY_10,
                         consumer_secret=TWITTER_API_SECRET_KEY_10,
                         access_token=TWITTER_ACCESS_TOKEN_10,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_10,
                         wait_on_rate_limit=True)

person11 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_11,
                         consumer_key=TWITTER_API_KEY_11,
                         consumer_secret=TWITTER_API_SECRET_KEY_11,
                         access_token=TWITTER_ACCESS_TOKEN_11,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_11,
                         wait_on_rate_limit=True)

person12 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_12,
                         consumer_key=TWITTER_API_KEY_12,
                         consumer_secret=TWITTER_API_SECRET_KEY_12,
                         access_token=TWITTER_ACCESS_TOKEN_12,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_12,
                         wait_on_rate_limit=True)

person13 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_13,
                         consumer_key=TWITTER_API_KEY_13,
                         consumer_secret=TWITTER_API_SECRET_KEY_13,
                         access_token=TWITTER_ACCESS_TOKEN_13,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_13,
                         wait_on_rate_limit=True)

person14 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_14,
                         consumer_key=TWITTER_API_KEY_14,
                         consumer_secret=TWITTER_API_SECRET_KEY_14,
                         access_token=TWITTER_ACCESS_TOKEN_14,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_14,
                         wait_on_rate_limit=True)

person15 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_15,
                         consumer_key=TWITTER_API_KEY_15,
                         consumer_secret=TWITTER_API_SECRET_KEY_15,
                         access_token=TWITTER_ACCESS_TOKEN_15,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_15,
                         wait_on_rate_limit=True)

person16 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_16,
                         consumer_key=TWITTER_API_KEY_16,
                         consumer_secret=TWITTER_API_SECRET_KEY_16,
                         access_token=TWITTER_ACCESS_TOKEN_16,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_16,
                         wait_on_rate_limit=True)

person17 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_17,
                         consumer_key=TWITTER_API_KEY_17,
                         consumer_secret=TWITTER_API_SECRET_KEY_17,
                         access_token=TWITTER_ACCESS_TOKEN_17,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_17,
                         wait_on_rate_limit=True)

person18 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_18,
                         consumer_key=TWITTER_API_KEY_18,
                         consumer_secret=TWITTER_API_SECRET_KEY_18,
                         access_token=TWITTER_ACCESS_TOKEN_18,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_18,
                         wait_on_rate_limit=True)

person19 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_19,
                         consumer_key=TWITTER_API_KEY_19,
                         consumer_secret=TWITTER_API_SECRET_KEY_19,
                         access_token=TWITTER_ACCESS_TOKEN_19,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_19,
                         wait_on_rate_limit=True)

person20 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_20,
                         consumer_key=TWITTER_API_KEY_20,
                         consumer_secret=TWITTER_API_SECRET_KEY_20,
                         access_token=TWITTER_ACCESS_TOKEN_20,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_20,
                         wait_on_rate_limit=True)

person21 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_21,
                         consumer_key=TWITTER_API_KEY_21,
                         consumer_secret=TWITTER_API_SECRET_KEY_21,
                         access_token=TWITTER_ACCESS_TOKEN_21,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_21,
                         wait_on_rate_limit=True)

person22 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_22,
                         consumer_key=TWITTER_API_KEY_22,
                         consumer_secret=TWITTER_API_SECRET_KEY_22,
                         access_token=TWITTER_ACCESS_TOKEN_22,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_22,
                         wait_on_rate_limit=True)

person23 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_23,
                         consumer_key=TWITTER_API_KEY_23,
                         consumer_secret=TWITTER_API_SECRET_KEY_23,
                         access_token=TWITTER_ACCESS_TOKEN_23,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_23,
                         wait_on_rate_limit=True)

person24 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_24,
                         consumer_key=TWITTER_API_KEY_24,
                         consumer_secret=TWITTER_API_SECRET_KEY_24,
                         access_token=TWITTER_ACCESS_TOKEN_24,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_24,
                         wait_on_rate_limit=True)

person25 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_25,
                         consumer_key=TWITTER_API_KEY_25,
                         consumer_secret=TWITTER_API_SECRET_KEY_25,
                         access_token=TWITTER_ACCESS_TOKEN_25,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_25,
                         wait_on_rate_limit=True)

person26 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_26,
                         consumer_key=TWITTER_API_KEY_26,
                         consumer_secret=TWITTER_API_SECRET_KEY_26,
                         access_token=TWITTER_ACCESS_TOKEN_26,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_26,
                         wait_on_rate_limit=True)

person27 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_27,
                         consumer_key=TWITTER_API_KEY_27,
                         consumer_secret=TWITTER_API_SECRET_KEY_27,
                         access_token=TWITTER_ACCESS_TOKEN_27,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_27,
                         wait_on_rate_limit=True)

person28 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_28,
                         consumer_key=TWITTER_API_KEY_28,
                         consumer_secret=TWITTER_API_SECRET_KEY_28,
                         access_token=TWITTER_ACCESS_TOKEN_28,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_28,
                         wait_on_rate_limit=True)

person29 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_29,
                         consumer_key=TWITTER_API_KEY_29,
                         consumer_secret=TWITTER_API_SECRET_KEY_29,
                         access_token=TWITTER_ACCESS_TOKEN_29,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_29,
                         wait_on_rate_limit=True)

person30 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_30,
                         consumer_key=TWITTER_API_KEY_30,
                         consumer_secret=TWITTER_API_SECRET_KEY_30,
                         access_token=TWITTER_ACCESS_TOKEN_30,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_30,
                         wait_on_rate_limit=True)

person31 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_31,
                         consumer_key=TWITTER_API_KEY_31,
                         consumer_secret=TWITTER_API_SECRET_KEY_31,
                         access_token=TWITTER_ACCESS_TOKEN_31,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_31,
                         wait_on_rate_limit=True)

person32 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_32,
                         consumer_key=TWITTER_API_KEY_32,
                         consumer_secret=TWITTER_API_SECRET_KEY_32,
                         access_token=TWITTER_ACCESS_TOKEN_32,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_32,
                         wait_on_rate_limit=True)

person33 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_33,
                         consumer_key=TWITTER_API_KEY_33,
                         consumer_secret=TWITTER_API_SECRET_KEY_33,
                         access_token=TWITTER_ACCESS_TOKEN_33,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_33,
                         wait_on_rate_limit=True)

person34 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_34,
                         consumer_key=TWITTER_API_KEY_34,
                         consumer_secret=TWITTER_API_SECRET_KEY_34,
                         access_token=TWITTER_ACCESS_TOKEN_34,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_34,
                         wait_on_rate_limit=True)

person35 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_35,
                         consumer_key=TWITTER_API_KEY_35,
                         consumer_secret=TWITTER_API_SECRET_KEY_35,
                         access_token=TWITTER_ACCESS_TOKEN_35,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_35,
                         wait_on_rate_limit=True)

person36 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_36,
                         consumer_key=TWITTER_API_KEY_36,
                         consumer_secret=TWITTER_API_SECRET_KEY_36,
                         access_token=TWITTER_ACCESS_TOKEN_36,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_36,
                         wait_on_rate_limit=True)

person37 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_37,
                         consumer_key=TWITTER_API_KEY_37,
                         consumer_secret=TWITTER_API_SECRET_KEY_37,
                         access_token=TWITTER_ACCESS_TOKEN_37,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_37,
                         wait_on_rate_limit=True)

person38 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_38,
                         consumer_key=TWITTER_API_KEY_38,
                         consumer_secret=TWITTER_API_SECRET_KEY_38,
                         access_token=TWITTER_ACCESS_TOKEN_38,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_38,
                         wait_on_rate_limit=True)

person39 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_39,
                         consumer_key=TWITTER_API_KEY_39,
                         consumer_secret=TWITTER_API_SECRET_KEY_39,
                         access_token=TWITTER_ACCESS_TOKEN_39,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_39,
                         wait_on_rate_limit=True)

person40 = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN_40,
                         consumer_key=TWITTER_API_KEY_40,
                         consumer_secret=TWITTER_API_SECRET_KEY_40,
                         access_token=TWITTER_ACCESS_TOKEN_40,
                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET_40,
                         wait_on_rate_limit=True)
