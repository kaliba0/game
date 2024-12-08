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
    """
    Efface l'écran du terminal.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def choisir_mot() -> str:
    """
    Choisit un mot au hasard depuis le fichier.
    :return: Le mot choisi.
    """
    with open(file, 'r') as f:
        mots = f.read().splitlines()
    return random.choice(mots)

def init_table() -> PrettyTable:
    """
    Initialise et retourne la table du tableau d'affichage.
    :return: Une instance de PrettyTable.
    """
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

def display_word(word: str, found_letters: set) -> str:
    """
    Affiche le mot avec les lettres trouvées et des '_' pour celles manquantes.
    :param word: Le mot à deviner.
    :param found_letters: Les lettres déjà trouvées.
    :return: Une chaîne avec les lettres trouvées et les '_' pour les manquantes.
    """
    return ' '.join([letter if letter in found_letters else '_' for letter in word])

def display_tested_letters(tested_letters: list[str]) -> str:
    """
    Affiche les lettres déjà testées.
    :param tested_letters: La liste des lettres déjà testées.
    :return: Une chaîne avec les lettres testées.
    """
    return ', '.join(sorted(tested_letters))

def display_status(word: str, found_letters: set, errors: int, tested_letters: list[str]):
    """
    Affiche l'état actuel du jeu.
    :param word: Le mot à deviner.
    :param found_letters: Les lettres déjà trouvées.
    :param errors: Le nombre d'erreurs commises.
    :param tested_letters: Les lettres déjà testées.
    """
    table = init_table()

    displayed_word = f"{GREEN_BOLD}{display_word(word, found_letters)}{RESET}"
    displayed_letters = f"{RED_BOLD}{display_tested_letters(tested_letters) or 'None'}{RESET}"
    pendu_display = f"{BLUE_BOLD}{max_errors - errors} errors remaining{RESET}\n{draw(errors)}"

    table.add_row([displayed_word, displayed_letters, pendu_display])
    clear_screen()
    print(table)

def save_game_state(state: dict):
    """
    Sauvegarde l'état actuel de la partie dans un fichier JSON.
    :param state: Dictionnaire contenant l'état du jeu.
    """
    with open(game_state_file, 'w') as f:
        json.dump(state, f)

def load_game_state() -> dict:
    """
    Charge et retourne l'état de la partie depuis le fichier JSON.
    :return: Dictionnaire contenant l'état du jeu.
    """
    with open(game_state_file, 'r') as f:
        return json.load(f)

def delete_saved_game():
    """
    Supprime le fichier de sauvegarde s'il existe.
    """
    if os.path.exists(game_state_file):
        os.remove(game_state_file)

def launch_game(state: dict = None):
    """
    Lance une partie de pendu, avec état existant ou nouveau.
    :param state: Dictionnaire contenant l'état du jeu ou None pour une nouvelle partie.
    """
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
            print(RED_BOLD + "Veuillez entrer une lettre valide !" + RESET)
            time.sleep(1)
            continue

        if letter in tested_letters:
            print(RED_BOLD + "Vous avez déjà testé cette lettre !" + RESET)
            time.sleep(1)
            continue

        tested_letters.append(letter)

        if letter in word:
            found_letters.add(letter)
            print(GREEN_BOLD + "Bien joué !" + RESET)
            time.sleep(1)
        else:
            errors += 1
            print(RED_BOLD + "Lettre incorrecte !" + RESET)
            time.sleep(1)

        if all([l in found_letters for l in word]):
            display_status(word, found_letters, errors, tested_letters)
            print(GREEN_BOLD + "Félicitations ! Vous avez gagné." + RESET)
            delete_saved_game()
            time.sleep(10)
            break
    else:
        display_status(word, found_letters, errors, tested_letters)
        print(RED_BOLD + f"Dommage ! Le mot était : {word}" + RESET)
        delete_saved_game()
        time.sleep(10)

def resume_game():
    """
    Reprend une partie précédemment mise en pause.
    """
    if not os.path.exists(game_state_file):
        print(RED_BOLD + "Aucune partie sauvegardée. Nouvelle partie commencée." + RESET)
        time.sleep(2)
        launch_game()
    else:
        state = load_game_state()
        launch_game(state)
