import random
from prettytable import PrettyTable
from pendu_ascii import draw
from fx.fx import clear_screen, choisir_mot
import time

RED_BOLD = '\033[1;91m'
GREEN_BOLD = '\033[1;32m'
BLUE_BOLD = '\033[1;34m'
RESET = '\033[0m'
BOLD = '\033[1m'

errors = 0
max_errors = 7
tested_letters = []

def init_table():
    table = PrettyTable()
    table.field_names = ["Word to Guess", "Tested Letters", "Pendu"]

    table.align["Word to Guess"] = "c"
    table.align["Tested Letters"] = "c"
    table.align["Pendu"] = "c"

    table.max_width["Word to Guess"] = 25
    table.max_width["Tested Letters"] = 20
    table.max_width["Pendu"] = 40

    table.hrules = 1
    table.junction_char = "╬"
    table.horizontal_char = "═"
    table.vertical_char = "║"
    table.horizontal_align_char = "═"

    return table

def display_word(word, found_letters):
    return ' '.join([letter if letter in found_letters else '_' for letter in word])

def display_tested_letters():
    return ', '.join(sorted(tested_letters))

def display_status(word, found_letters):
    table = init_table()

    displayed_word = f"{GREEN_BOLD}{display_word(word, found_letters)}{RESET}"
    displayed_letters = f"{RED_BOLD}{display_tested_letters() or 'None'}{RESET}"
    pendu_display = f"{BLUE_BOLD}{max_errors - errors} errors remaining{RESET}\n{draw(errors)}"

    table.add_row([displayed_word, displayed_letters, pendu_display])
    clear_screen()
    print(table)

def launch_game():
    global errors, tested_letters
    errors = 0
    tested_letters = []
    word = choisir_mot().upper()
    found_letters = set()

    while errors < max_errors:
        display_status(word, found_letters)

        letter = input("Letter to guess? ").upper()
        if not letter.isalpha() or len(letter) != 1:
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
            display_status(word, found_letters)
            print(GREEN_BOLD + "Congratulations! You won." + RESET)
            break
    else:
        display_status(word, found_letters)
        print(RED_BOLD + f"Too bad! The word was: {word}" + RESET)
