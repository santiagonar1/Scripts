#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

MILLISECONDS_IN_HOUR = 3600000
MILLISECONDS_IN_MINUTE = 60000
MILLISECONDS_IN_SECOND = 1000

class Time():
    """
    Represents a time object.
    attributes: hour, minute, second, millisecond
    """
    def __init__(self, hour=0, minute=0, second=0, millisecond=0):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.millisecond = millisecond

    def __int__(self):
        """
        The integer representation of Time is equal to the number of
        milliseconds
        """
        milliseconds = (self.hour * MILLISECONDS_IN_HOUR +
        self.minute * MILLISECONDS_IN_MINUTE +
        self.second * MILLISECONDS_IN_SECOND +
        self.millisecond)
        return milliseconds

    def __le__(self, other):
        return int(self) <= int(other)

    def __lt__(self, other):
        return int(self) < int(other)

    def __ge__(self, other):
        return int(self) >= int(other)

    def __gt__(self, other):
        return int(self) > int(other)

    def __add__(self, other):
        """
        The sum is equal to the total number of milliseconds
        """
        return int(self) + int(other)

    def __sub__(self, other):
        """
        The substraction is equal to the substraction of the number of
        milliseconds of each Time.

        The result must be a positive number. In case other > self, an
        AssertionError will be raised
        """
        assert self >= other
        return int(self) - int(other)

    def __str__(self):
        """
        The representation of a Time variable is HH:MM:SS,mmm
        """
        return "{0.hour:0>2}:{0.minute:0>2}:{0.second:0>2},{0.millisecond:0>3}".format(self)

def milliseconds_to_time(milliseconds):
    """
    Makes a new Time object.
    milliseconds: int milliseconds since midnight.
    """
    time = Time()
    time.hour, minutes = divmod(milliseconds, MILLISECONDS_IN_HOUR)
    time.minute, seconds = divmod(minutes, MILLISECONDS_IN_MINUTE)
    time.second, time.millisecond = divmod(seconds, MILLISECONDS_IN_SECOND)
    return time

def validate_string(string):
    """
    Checks whether the string has the correct format for a time variable or not
    """
    return re.match("\d\d:\d\d:\d\d,\d\d\d", string) and len(string) == 12

def string_to_time(string):
    """
    Transform a string with format HH:MM:SS,mmm into a time object
    """
    assert validate_string(string)
    time = Time()
    time.hour = int(string[0:2])
    time.minute = int(string[3:5])
    time.second = int(string[6:8])
    time.millisecond = int(string[9:12])
    return time

