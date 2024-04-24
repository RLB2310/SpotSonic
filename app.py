import curses
import signal
from menu import Menu

def main():
    menu = Menu()

    def handle_resize(signum, frame):
        curses.endwin()  # End current curses session
        curses.initscr()  # Re-initialize
        curses.cbreak()  # Required for curses
        curses.noecho()  # Prevent character echo
        menu = Menu()  # Re-create the menu instance to reset the state
        menu.navigate_menu()  # Start again
    # Set up signal handler for resizing
    signal.signal(signal.SIGWINCH, handle_resize)

    menu.navigate_menu()

if __name__ == "__main__":
    main()

