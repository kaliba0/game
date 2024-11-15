import random
from prettytable import PrettyTable
import os
from pendu_ascii import draw


RED_BOLD = '\033[1;91m'
GREEN_BOLD = '\033[1;32m'
BLUE_BOLD = '\033[1;34m'
RESET = '\033[0m'
BOLD = '\033[1m'

file = 'words.txt'
errors = 0
max_errors = 7
tested_letters = []


def choisir_mot():
    with open(file, 'r') as f:
        mots = f.read().splitlines()
    return random.choice(mots)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')