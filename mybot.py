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

BOTNAME = "Coolbot"

NONSPEC_RESPONSES = [
    "Uh whatever",
    "Lol",
    "I understand",
    "Got ya",
    "I get your point",
    "Wanna talk about anything else?",
    "Code hard",
    "Why don't you go write some code?",
    "Uh I see.",
    "Let's have some coffee",
    "It's fun talking to you",
    "So what?",
    "What are you up to?",
    "How's your day going?",
    "Fair enough.",
    "Oh okay"
]

GREETINGS = [
    "hi",
    "hi there",
    "hello",
    "hey",
    "hey there",
    "what's up",
    "whats up",
    "sup",
]

GREET_RESPONSES = [
    "Hey!",
    "Hi!",
    "Hi there!",
    "Hello",
    "What's up?",
    "Hey friend",
]

HOWRU = [
    "how are you",
    "how r u",
    "how are you doing",
    "how have you been",
    "how are you doing today",
    "how is your day going"
]

GOODBYE = [
    "bye",
    "goodbye",
    "bye bye",
    "see ya",
    "later",
    "sweet dreams",
    "i gotta go",
    "good night"
]

GOODBYE_RESP = [
    "Goodbye",
    "Bye bye!",
    "Bye!",
    "Later",
    "See you",
    "See you later"
]

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


if __name__ == "__main__":

    YOURNAME = input("What's your name?\n")

    GREETING = respond("Hey {}, what's up? I am Coolbot, welcome to the chat!\
    It's nice to see you here!".format(YOURNAME))

    prev_reply = ["", "", ""]

    while True:

        user_msg = input("{} {}::  ".format(YOURNAME, addspace()["user_msg"]))
        timestamp2 = time.asctime()[11:19]
        print(" "  * 50 + "/" + timestamp2)
        if not user_msg[-1].isalpha():
            user_msg = user_msg[0:-1]


        if check_membership(user_msg, GREETINGS):
                response = random.choice(GREET_RESPONSES)
                respond(response)

        elif check_membership(user_msg, HOWRU):
            response = "I'm good. You?"
            respond(response)

        elif check_membership(user_msg, GOODBYE):
            response = random.choice(GOODBYE_RESP)
            respond(response)
            sys.exit()


        else:
            while True:
                response = random.choice(NONSPEC_RESPONSES)
                if response not in prev_reply:
                    break
            prev_reply[0], prev_reply[1], prev_reply[2] = prev_reply[1],\
                                                    prev_reply[2], response
            respond(response)
