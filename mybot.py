#!/usr/bin/python3
"""
Chatbot for live chatting in terminal
Informal, casual, uses slang
Run 'python3 mybot.py'
Exit with Ctrl+D or say goodbye
"""

import os
import time
import sys
import random
import nltk
import string
import logging

from responses import *

# Logging
logging.basicConfig(filename='mybot.log', level=logging.DEBUG,
                    format='%(asctime)s:  %(name)s: %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Used for generating daytime-specific comments
DAYTIME_CHOICE = "daytime choice"

# Name of the bot shown in the dialog window
BOTNAME = "Coolbot"

# List of punctuation characters to be removed from text
PUNCT = list(string.punctuation)
PUNCT.pop(PUNCT.index("'"))

def preprocess(user_msg):
    """
    Input: user input string
    Output: 1st sentence of user input, lowercase, without punctuation
    """
    user_msg = nltk.sent_tokenize(user_msg)
    user_msg = user_msg[0]
    user_msg = [ch for ch in user_msg if ch not in PUNCT]
    user_msg = "".join(user_msg)
    user_msg = user_msg.lower()
    return user_msg

def check_membership(user_msg, user_kwds):
    """
    Input: user input string, list of user message keywords
    Output: boolean
    Check if user input contains a keyword from the list
    """
    user_msg = preprocess(user_msg)
    for msg in user_kwds:
        if len(msg.split()) == 1:
            user_msg_lst = nltk.word_tokenize(user_msg)
            if msg in user_msg_lst:
                return True
                break
        elif msg in user_msg:
            return True
            break
    return False


def addspace():
    """
    Get additional space characters
    in order to align bot and user names of different length
    """
    if len(YOURNAME) < len(BOTNAME):
        space = " " * (len(BOTNAME) - len(YOURNAME))
        return {"user_msg": space, "r": ""}
    elif len(YOURNAME) > len(BOTNAME):
        space = " " * (len(YOURNAME) - len(BOTNAME))
        return {"user_msg": "", "r": space}
    return {"user_msg": "", "r": ""}


def respond(response):
    """
    Build response output template
    Not including the response message
    """
    timestamp =  time.asctime()[11:19]
    print(BOTNAME + " {}::  ...".format(addspace()["r"]))
    time.sleep(1)
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
    timestamp =  time.asctime()[11:19]
    print(BOTNAME + " {}::  {}".format(addspace()["r"], response))
    print(" "  * 50 + "/" + timestamp)

def daytime_response():
    """
    Check if it's morning/afternoon/evening/night
    and choose an appropriate question to ask
    Output: question string
    """
    timestamp = time.asctime()[11:16]
    if timestamp > "07:00" and timestamp <= "12:00":
        resp_choice = MORNING_RESP
    elif timestamp > "12:00" and timestamp <= "18:30":
        resp_choice = AFTERNOON_RESP
    elif (timestamp > "18:30" and timestamp <= "23:59") or timestamp <= "01:00":
        resp_choice = EVENING_RESP
    else:
        resp_choice = NIGHT_RESP
    return random.choice(resp_choice)

if __name__ == "__main__":

    YOURNAME = input(NAME_PROMPT)

    logger.info(f"Conversation started with {YOURNAME}")

    GREETING = respond(INIT_GREET.format(**{"user": YOURNAME, "bot": BOTNAME}))

    # Store previous replies in order to avoid repetion
    prev_reply = ["", "", ""]

    while True:

        try:

            # Print out the user input prompt and let user type in their message
            user_msg = input("{} {}::  ".format(YOURNAME, addspace()["user_msg"]))
            timestamp = time.asctime()[11:19]
            print(" "  * 50 + "/" + timestamp)
            if not user_msg[-1].isalpha():
                user_msg = user_msg[0:-1]

            # Look up keywords to select an appropriate reply

            if check_membership(user_msg, GREETINGS):
                response = random.choice(GREET_RESPONSES)

            elif check_membership(user_msg, HOWRU):
                response = random.choice(HOWRU_RESP)

            elif check_membership(user_msg, THANKS):
                response = random.choice(THANKS_RESP)

            elif check_membership(user_msg, GOODBYE):
                response = random.choice(GOODBYE_RESP)

            # If no keywords were matched, select a random reply

            else:
                while True:
                    response = random.choice(NONSPEC_RESPONSES)
                    # if a daytime-specific reply was randomly chosen,
                    # determine the current time of the day
                    # and select an appropriate comment
                    if response == DAYTIME_CHOICE:
                        response = daytime_response()
                    if response not in prev_reply:
                        break
                prev_reply[0], prev_reply[1], prev_reply[2] = prev_reply[1],\
                                                        prev_reply[2], response
            respond(response)

            # If user said goodbye, quit the script
            if check_membership(user_msg, GOODBYE):
                logger.info("User said goodbye, conversation terminated")
                sys.exit()

        # Exit with Ctrl-C
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt, conversation terminated")
            sys.exit()

        # Exit with Ctrl-D
        except EOFError:
            logger.info("End of user input, conversation terminated")
            sys.exit()
