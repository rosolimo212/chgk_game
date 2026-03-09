import random
import numpy as np
import pandas as pd
import datetime


def get_d20():
    """
    Generate a random number between 1 and 20
    """
    return random.randint(1, 20)

def get_d100():
    """
    Generate a random number between 1 and 100
    """
    return random.randint(1, 100)

def try_d100(difficulty):
    """
    Returns 1 or 0 with a probability of difficulty
    """
    if random.randint(1, 100) >= difficulty:
        return 1
    else:
        return 0


