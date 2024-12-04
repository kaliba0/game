import random
from prettytable import PrettyTable
import os
from pendu_ascii import draw
import time
import json

RED_BOLD = '\033[1;91m'
GREEN_BOLD = '\033[1;32m'
BLUE_BOLD = '\033[1;34m'
RESET = '\033[0m'
BOLD = '\033[1m'

file = os.path.join(os.path.dirname(__file__), 'words.txt')
game_state_file = os.path.join(os.path.dirname(__file__), 'saved_game.json')

if not os.path.exists(file):
    print(f"Le fichier '{file}' est introuvable.")
    exit(1)

max_errors = 7

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def choisir_mot():
    with open(file, 'r') as f:
        mots = f.read().splitlines()
    return random.choice(mots)

def init_table():
    table = PrettyTable()
    table.field_names = [f"{GREEN_BOLD}Word to Guess{RESET}", f"{RED_BOLD}Tested Letters{RESET}", f"{BLUE_BOLD}Pendu{RESET}"]

    table.align[f"{GREEN_BOLD}Word to Guess{RESET}"] = "c"
    table.align[f"{RED_BOLD}Tested Letters{RESET}"] = "c"
    table.align[f"{BLUE_BOLD}Pendu{RESET}"] = "c"
    table.min_width[f"{GREEN_BOLD}Word to Guess{RESET}"] = 25
    table.min_width[f"{RED_BOLD}Tested Letters{RESET}"] = 20
    table.min_width[f"{BLUE_BOLD}Pendu{RESET}"] = 30
    table.max_width[f"{GREEN_BOLD}Word to Guess{RESET}"] = 35
    table.max_width[f"{RED_BOLD}Tested Letters{RESET}"] = 30
    table.max_width[f"{BLUE_BOLD}Pendu{RESET}"] = 50

    table.hrules = 1
    table.junction_char = "+"
    table.horizontal_char = "═"
    table.vertical_char = "║"

    return table

def display_word(word, found_letters):
    return ' '.join([letter if letter in found_letters else '_' for letter in word])

def display_tested_letters(tested_letters):
    return ', '.join(sorted(tested_letters))

def display_status(word, found_letters, errors, tested_letters):
    table = init_table()

    displayed_word = f"{GREEN_BOLD}{display_word(word, found_letters)}{RESET}"
    displayed_letters = f"{RED_BOLD}{display_tested_letters(tested_letters) or 'None'}{RESET}"
    pendu_display = f"{BLUE_BOLD}{max_errors - errors} errors remaining{RESET}\n{draw(errors)}"

    table.add_row([displayed_word, displayed_letters, pendu_display])
    clear_screen()
    print(table)

def save_game_state(state):
    with open(game_state_file, 'w') as f:
        json.dump(state, f)

def load_game_state():
    with open(game_state_file, 'r') as f:
        return json.load(f)

def delete_saved_game():
    if os.path.exists(game_state_file):
        os.remove(game_state_file)

def launch_game(state=None):
    if state:
        errors = state['errors']
        tested_letters = state['tested_letters']
        word = state['word']
        found_letters = set(state['found_letters'])
    else:
        delete_saved_game()
        errors = 0
        tested_letters = []
        word = choisir_mot().upper()
        found_letters = set()

    while errors < max_errors:
        display_status(word, found_letters, errors, tested_letters)

        letter = input("Letter to guess? ").upper()
        if letter.lower() == 'pause':
            game_state = {
                'errors': errors,
                'tested_letters': tested_letters,
                'word': word,
                'found_letters': list(found_letters)
            }
            save_game_state(game_state)
            print(BLUE_BOLD + "Game paused. Returning to menu." + RESET)
            time.sleep(2)
            return
        elif not letter.isalpha() or len(letter) != 1:
            print(RED_BOLD + "Please enter a single valid letter!" + RESET)
            time.sleep(1)
            continue

        if letter in tested_letters:
            print(RED_BOLD + "You have already tried this letter!" + RESET)
            time.sleep(1)
            continue

        tested_letters.append(letter)

        if letter in word:
            found_letters.add(letter)
            print(GREEN_BOLD + "Well done!" + RESET)
            time.sleep(1)
        else:
            errors += 1
            print(RED_BOLD + "Incorrect letter!" + RESET)
            time.sleep(1)

        if all([letter in found_letters for letter in word]):
            display_status(word, found_letters, errors, tested_letters)
            print(GREEN_BOLD + "Congratulations! You won." + RESET)
            delete_saved_game()
            time.sleep(10)
            break
    else:
        display_status(word, found_letters, errors, tested_letters)
        print(RED_BOLD + f"Too bad! The word was: {word}" + RESET)
        delete_saved_game()
        time.sleep(10)

def resume_game():
    if not os.path.exists(game_state_file):
        print(RED_BOLD + "No saved game found. Starting a new game." + RESET)
        time.sleep(2)
        launch_game()
    else:
        state = load_game_state()
        launch_game(state)
