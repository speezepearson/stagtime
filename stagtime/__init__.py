"""Implementation of the TagTime Universal Ping Schedule
Spec: https://forum.beeminder.com/t/official-reference-implementation-of-the-tagtime-universal-ping-schedule/4282
"""

import math

GAP = 45*60         # Average gap between pings, in seconds
URPING = 1184097393 # Ur-ping ie the birth of Timepie/TagTime! (unixtime)
SEED   = 11193462   # Initial state of the random number generator
IA = 16807          # =7^5: Multiplier for LCG random number generator
IM = 2147483647     # =2^31-1: Modulus used for the RNG

# Above URPING is in 2007 and it's fine to jump to any later URPING/SEED pair
# like this one in 2018 -- URPING = 1532992625, SEED = 75570 -- without
# deviating from the universal ping schedule.

class Timekeeper:
    def __init__(self):
        self.pung = URPING # Global var with unixtime (in seconds) of last computed ping
        self.state = SEED  # Global variable that's the state of the RNG



    # Here are the functions for generating random numbers in general:

    # Linear Congruential Generator, returns random integer in {1, ..., IM-1}.
    # This is ran0 from Numerical Recipes and has a period of ~2 billion.
    def lcg(self):
        self.state = IA * self.state % IM  # lcg()/IM is a U(0,1) R.V.
        return self.state

    # Return a random number drawn from an exponential distribution with mean m
    def exprand(self, m):
        return -m * math.log(self.lcg()/IM)




    # Here’s the only other helper function we need:

    # Every TagTime gap must be an integer number of seconds not less than 1
    def gap(self):
        return max(1, round(self.exprand(GAP)))





    # And here are the functions to compute successive ping times:

    # Return unixtime of the next ping. First call init(t) and then call this in
    # succession to get all the pings starting with the first one after time t.
    def nextping(self):
        self.pung += self.gap()
        return self.pung

    # Start at the beginning of time and walk forward till we hit the first ping
    # strictly after time t. Then scooch the state back a step and return the first
    # ping *before* (or equal to) t. Then we're ready to call nextping().
    def init(self, t):
        [self.pung, self.state] = [URPING, SEED]  # reset the global state
        while self.pung <= t:
            [p, s] = [self.pung, self.state]      # walk forward
            self.nextping()
        [self.pung, self.state] = [p, s]          # rewind a step
        return self.pung                          # return most recent ping time <= t


    # Protypical usage is like so:

    # p = init(now)
    # print "Welcome to TagTime! Last ping would've been at time {p}."
    # repeat forever: \
    # p = nextping()
    # while now < p: wait
    # print "PING! What are you doing right now, at time {p}?"
