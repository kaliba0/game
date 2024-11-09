import random
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


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def choisir_mot():
    with open(file, 'r') as f:
        mots = f.read().splitlines()
    return random.choice(mots)

def afficher_mot(mot, lettres_trouvees):
    return ' '.join([lettre if lettre in lettres_trouvees else '_' for lettre in mot])

def afficher_lettres_testees():
    return ', '.join(tested_letters)

def afficher_statut(mot, lettres_trouvees):
    # Clear screen and display the structured interface
    clear_screen()
    
    # Mot à deviner (en haut à gauche)
    print("╔══════════════════════════════════════════════╗")
    print("║               MOT À DEVINER                 ║")
    print("╠══════════════════════════════════════════════╣")
    print(f"║ {GREEN_BOLD} {afficher_mot(mot, lettres_trouvees)} {RESET}")
    print("╚══════════════════════════════════════════════╝")
    
    # Lettres testées (en bas à gauche)
    print("╔══════════════════════════════════════════════╗")
    print("║               LETTRES TESTÉES                ║")
    print("╠══════════════════════════════════════════════╣")
    print(f"║ {RED_BOLD} {afficher_lettres_testees()} {RESET}")
    print("╚══════════════════════════════════════════════╝")
    
    # Nombre d'essais restants et le dessin du pendu (à droite)
    print("╔══════════════════════════════════════════════╗")
    print("║         NOMBRE D'ESSAIS RESTANTS             ║")
    print("╠══════════════════════════════════════════════╣")
    print(f"║ {BLUE_BOLD} {max_errors - errors} {RESET}")
    print("╚══════════════════════════════════════════════╝")
    
    print("╔══════════════════════════════════════════════╗")
    print("║               DESSIN DU PENDU                ║")
    print("╠══════════════════════════════════════════════╣")
    print(draw(errors))  # Always show the initial drawing even if no errors
    print("╚══════════════════════════════════════════════╝")

def launch_game():
    global errors, tested_letters
    errors = 0
    tested_letters = []
    mot = choisir_mot()
    lettres_trouvees = set()

    while errors < max_errors:
        afficher_statut(mot, lettres_trouvees)

        lettre = input("Lettre à tester ? ").upper()
        if lettre in tested_letters:
            print(RED_BOLD + "Vous avez déjà essayé cette lettre !" + RESET)
            continue

        tested_letters.append(lettre)

        if lettre in mot:
            lettres_trouvees.add(lettre)
            print(GREEN_BOLD + "Bien joué !" + RESET)
        else:
            errors += 1
            print(RED_BOLD + "Lettre incorrecte !" + RESET)

        if all([lettre in lettres_trouvees for lettre in mot]):
            afficher_statut(mot, lettres_trouvees)
            print(GREEN_BOLD + "Félicitations ! Vous avez gagné." + RESET)
            break

    else:
        afficher_statut(mot, lettres_trouvees)
        print(RED_BOLD + "Dommage ! Le mot était : " + mot + RESET)
