import os
from fx import launch_game, clear_screen, resume_game

RED_BOLD = '\033[1;91m'
BOLD = '\033[1m'
RESET = '\033[0m'
BLUE_BOLD = '\033[1;34m'

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

    infos = f'    {BOLD} CREATED ON 11/24 BY {BLUE_BOLD}ANTOINE & KILLIAN {RESET}'
    print(banner)
    print(infos)

def show_menu():
    menu = BOLD + """

    =============== OPTIONS ===============

             1.  Start a new game
            2.  Continue your game
    """ + RESET
    print(menu)

def main():
    clear_screen()
    show_banner()
    show_menu()

    while True:
        choice = input(RED_BOLD + 'pendu/menu> ' + RESET)
        if choice.strip() == '1':
            clear_screen()
            launch_game()
            clear_screen()
            show_banner()
            show_menu()
        elif choice.strip() == '2':
            clear_screen()
            resume_game()
            clear_screen()
            show_banner()
            show_menu()
        else:
            print(RED_BOLD + "INVALID CHOICE. PLEASE TRY AGAIN" + RESET)

if __name__ == "__main__":
    main()
