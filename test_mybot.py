#!/usr/bin/python3
import unittest

from mybot import *
from responses import *


class TestMybot(unittest.TestCase):

    def test_preprocess(self):

        msg = preprocess("Great, things seem to be working out now.")
        result = "great things seem to be working out now"
        self.assertEqual(msg, result)

    def test_lookup(self):

        msg1 = "nope but thanks for the suggestion"
        result1 = lookup(msg1, THANKS)
        self.assertTrue(result1)

        msg2 = "me too"
        result2 = lookup(msg2, GREETINGS)
        self.assertFalse(result2)


    def test_respond(self):

        msg1 = "Hi, how is it going?"
        result1 = respond(msg1)
        self.assertIn(result1, GREET_RESPONSES)

        msg2 = "How've you been?"
        result2 = respond(msg2)
        self.assertIn(result2, HOWRU_RESP)

        msg3 = "Thanks for asking!"
        result3 = respond(msg3)
        self.assertIn(result3, THANKS_RESP)

        msg4 = "You're not supposed to do this"
        while True:
            result4 = respond(msg4)
            if result4 != DAYTIME_CHOICE:
                break
        self.assertIn(result4, NONSPEC_RESPONSES)

        msg5 = "Bye bye dear bot!"
        result5 = respond(msg5)
        self.assertIn(result5, GOODBYE_RESP)



if __name__ == '__main__':
    unittest.main()
