#!/usr/bin/python3
"""
Chatbot for live chatting in terminal
Informal, casual, uses slang
Run 'python3 mybot.py'
Exit with  Ctrl+C, Ctrl+D or say goodbye
"""

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

# Store previous replies in order to avoid repetition
prev = ['', '', '']

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

def lookup(user_msg, user_kwds):
    """
    Input: user input string, list of user message keywords
    Output: boolean
    Check if user input contains a keyword from the list
    """
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


def format_response(response):
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

def get_user_input():
    """
    Print out the user input prompt and let user type in their message
    Print out the timestamp
    Output: unprocessed user message as string
    """
    user_msg = input("{} {}::  ".format(YOURNAME, addspace()["user_msg"]))
    timestamp = time.asctime()[11:19]
    print(" "  * 50 + "/" + timestamp)
    return user_msg


def respond(user_msg):
    """Process the user message and select an appropriate response"""

    user_msg = preprocess(user_msg)

    global prev

    while True:

        # Look up keywords to select an appropriate reply

        if lookup(user_msg, GREETINGS):
            response = random.choice(GREET_RESPONSES)

        elif lookup(user_msg, HOWRU):
            response = random.choice(HOWRU_RESP)

        elif lookup(user_msg, THANKS):
            response = random.choice(THANKS_RESP)

        elif lookup(user_msg, GOODBYE):
            response = random.choice(GOODBYE_RESP)

        # If no keywords were matched, select a random reply

        else:
            response = random.choice(NONSPEC_RESPONSES)
            # if a daytime-specific reply was randomly chosen,
            # determine the current time of the day
            # and select an appropriate comment
            if response == DAYTIME_CHOICE:
                response = daytime_response()

        if response not in prev:
            break

    prev[0], prev[1], prev[2] = prev[1], prev[2], response

    return response


if __name__ == "__main__":

    YOURNAME = input(NAME_PROMPT)

    logger.info(f"Conversation started with {YOURNAME}")

    GREETING = format_response(INIT_GREET.format(**{"user": YOURNAME, "bot": BOTNAME}))

    while True:

        try:

            # Print out the user input prompt and let user type in their message
            user_msg = get_user_input()

            # Process the message and select a response
            response = respond(user_msg)

            # Print out bot's response in a formatted way
            format_response(response)

            # If user said goodbye, quit the script
            if response in GOODBYE_RESP:
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
