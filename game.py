import os 
import random

RED_BOLD = '\033[1;91m'
BOLD = '\033[1m'
RESET = '\033[0m'
BLUE_BOLD = '\033[1;34m'
GREEN_BOLD = '\033[1;32m'

errors= 0

file = 'words.txt'

def choisir_mot():
    with open(file, 'r') as f:
        mots = f.read().splitlines()

    word = random.choice(mots)
    return word

def tirets(mot):
    for k in mot:
        print(f'{BOLD}_', end=" ")
    print(f'{RESET}')

def launch_game():
    correct = choisir_mot()
    print(correct)
    tirets(correct)
    