import os
from game import launch_game

RED_BOLD = '\033[1;91m'
BOLD = '\033[1m'
RESET = '\033[0m'
BLUE_BOLD = '\033[1;34m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    banner = RED_BOLD + """
╔───────────────────────────────────────────────╗
│                                               │
│  ██████╗ ███████╗███╗   ██╗██████╗ ██╗   ██╗  │
│  ██╔══██╗██╔════╝████╗  ██║██╔══██╗██║   ██║  │
│  ██████╔╝█████╗  ██╔██╗ ██║██║  ██║██║   ██║  │
│  ██╔═══╝ ██╔══╝  ██║╚██╗██║██║  ██║██║   ██║  │
│  ██║     ███████╗██║ ╚████║██████╔╝╚██████╔╝  │
│  ╚═╝     ╚══════╝╚═╝  ╚═══╝╚═════╝  ╚═════╝   │
│                                               │
╚───────────────────────────────────────────────╝
    """ + RESET

    infos = f'{BOLD} CREATED ON 11/24 BY {BLUE_BOLD} ANTOINE {RED_BOLD} (NOT KILLIAN) {RESET}'
    print(banner)
    print(infos)

def show_menu():
    menu = BOLD + """

    =============== OPTIONS ===============

             1.  Start a new game
            2.  Continue your game
    """ + RESET
    print(menu)

def update_prompt(state):
    if state == "menu":
        return RED_BOLD + 'pendu/menu> ' + RESET
    elif state == "ingame":
        return 'Lettre à tester ? '

def main():
    prompt = update_prompt("menu")
    clear_screen()
    show_banner()
    show_menu()

    while True:
        choice = input(prompt)
        if choice.strip() == '1':
            clear_screen()
            launch_game()
            prompt = update_prompt("ingame")
        else:
            print(RED_BOLD + "INVALID CHOICE. PLEASE TRY AGAIN" + RESET)

if __name__ == "__main__":
    main()
