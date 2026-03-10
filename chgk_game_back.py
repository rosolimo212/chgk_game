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
    if get_d100() >= difficulty:
        return 1
    else:
        return 0



# series in n tryes to get a border
def make_qv(difficulty, n_try):
    """
    Make a series of n tries to get a border
    """
    res = 0
    res_lst = []
    for i in n_try:
        tr_iter = get_d100()
        res_lst.append(tr_iter)
        if tr_iter >= difficulty:
            res = 1
            break
    return res, res_lst