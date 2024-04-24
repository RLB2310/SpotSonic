import os
import curses
from spotify_controller import SpotifyController
from search import Search
import time
import numpy as np
import pyaudio



class Menu:
    def __init__(self):
        self.spotify = SpotifyController()
        self.search_instance = Search()
        self.recently_played_artists = self.load_recent_artists()  # Load recent artists from 'recent.txt'
        self.current_section = None  # No section selected by default
        self.current_artist_pos = 0  # Position in 'Recently Played'
        self.initialize_curses()

    def initialize_curses(self):
        self.stdscr = curses.initscr()
        curses.cbreak()
        curses.noecho()
        self.stdscr.keypad(True)
        self.stdscr.refresh()


    def cleanup_curses(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.endwin()

    def load_recent_artists(self):
        """Load recently played artists from 'recent.txt'"""
        if os.path.exists("recent.txt"):
            with open("recent.txt", "r") as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        else:
            return []

    def display_recently_played(self, win):
        """Display the list of recently played artists in the specified window."""
        win.clear()
        win.border(0)
        win.addstr(1, 1, "Recently Played:")

        # Display 'Recently Played' artists
        for idx, artist in enumerate(self.recently_played_artists, 1):
            if idx - 1 == self.current_artist_pos:
                win.addstr(1 + idx, 1, f"> {artist}", curses.A_REVERSE)
            else:
                win.addstr(1 + idx, 1, artist)

        win.refresh()

    def navigate_menu(self):
        """Navigate and display the main menu with sections."""
        height, width = self.stdscr.getmaxyx()
        min_width = 40
        min_height = 10

        if height < min_height or width < min_width:
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, f"Terminal too small. Requires at least {min_width}x{min_height}.")
            self.stdscr.refresh()
            return

        self.stdscr.clear()
        self.stdscr.refresh()

        # Define sections and draw borders
        search_bar_height = 2
        menu_height = height - search_bar_height - 2  # Leave room for 'Now Playing'
        recently_played_width = int(width * 0.25)

        search_bar_win = curses.newwin(search_bar_height, width, 0, 0)
        menu_win = curses.newwin(menu_height, width - recently_played_width, search_bar_height, 0)
        recently_played_win = curses.newwin(menu_height, recently_played_width, search_bar_height, width - recently_played_width)
        now_playing_win = curses.newwin(2, width, height - 2, 0)
        # Draw section borders
        search_bar_win.border(0)
        menu_win.border(0)
        recently_played_win.border(0)
        now_playing_win.border(0)

        # Add static labels and content
        search_bar_win.addstr(1, 1, "Search:")
        now_playing_win.addstr(1, 1, "Now Playing: ")

        # Display 'Recently Played' artists using the new method
        self.display_recently_played(recently_played_win)

        # Refresh all windows
        search_bar_win.refresh()
        menu_win.refresh()
        recently_played_win.refresh()
        now_playing_win.refresh()

        # Update 'Now Playing'
        self.update_now_playing(now_playing_win)

        # Start navigation
        self.handle_navigation(search_bar_win, menu_win, recently_played_win, now_playing_win)
    def update_now_playing(self, win):
        """Update the 'Now Playing' section with the current song."""
        current_song = self.spotify.get_current_playing()  # Get current playing track
        win.clear()
        win.border(0)
        win.addstr(1, 1, f"Now Playing: {current_song}")
        win.refresh()


    def handle_navigation(self, search_bar_win, menu_win, recently_played_win, now_playing_win):
        """Handle navigation between sections and control playback."""
        while True:
            key = self.stdscr.getch()

            # Determine which section to navigate based on the current selection
            if self.current_section is None:
                if key == ord('s'):  # Select search section
                    self.current_section = "search"
                    self.search_bar(search_bar_win, menu_win, now_playing_win, recently_played_win)
                elif key == ord('r'):  # Select recently played section
                    self.current_section = "recent"
                    self.recently_played_navigation(recently_played_win, now_playing_win)
            elif self.current_section == "search":
                if key == 27:  # Escape to deselect
                    self.current_section = None
                else:
                    self.search_bar(search_bar_win, menu_win, now_playing_win, recently_played_win)
            elif self.current_section == "recent":
                if key == 27:  # Escape to deselect
                    self.current_section = None
                else:
                    self.recently_played_navigation(recently_played_win, now_playing_win)

            # Global playback controls when no section is selected
            if self.current_section is None:
                if key == ord('p'):  # Play/Pause
                    self.spotify.play_pause()
                elif key == ord('l'):  # Next track
                    self.spotify.next()
                elif key == ord('h'):  # Previous track
                    self.spotify.prev()
                elif key == ord('q'):  # Quit the app
                    break

    def recently_played_navigation(self, recently_played_win, now_playing_win):
        """Navigate the 'Recently Played' section."""
        max_pos = len(self.recently_played_artists) - 1

        while True:
            recently_played_win.clear()
            recently_played_win.border(0)
            recently_played_win.addstr(1, 1, "Recently Played:")

            for idx, artist in enumerate(self.recently_played_artists, 1):
                if idx - 1 == self.current_artist_pos:
                    recently_played_win.addstr(1 + idx, 1, f"> {artist}", curses.A_REVERSE)
                else:
                    recently_played_win.addstr(1 + idx, 1, artist)

            recently_played_win.refresh()

            key = self.stdscr.getch()

            if key == 27:  # Escape to deselect
                self.current_section = None
                break
            elif key in [curses.KEY_DOWN, ord('j')]:  # Navigate down
                self.current_artist_pos = min(self.current_artist_pos + 1, max_pos)
            elif key in [curses.KEY_UP, ord('k')]:  # Navigate up
                self.current_artist_pos = max(self.current_artist_pos - 1, 0)
            elif key == ord('\n'):  # Enter to select artist
                selected_artist = self.recently_played_artists[self.current_artist_pos]
                # Play the most recent track by this artist or take other action
                self.spotify.play_artist(selected_artist)
                self.update_now_playing(now_playing_win)
                break

    def search_bar(self, search_bar_win, menu_win, now_playing_win, recently_played_win):
        """Handle text-based search and navigation."""
        search_text = ""
        in_search = True
        while in_search:
            key = self.stdscr.getch()

            if key == 27:  # Escape key to exit search
                in_search = False
            elif key in (curses.KEY_BACKSPACE, 127):  # Backspace to delete characters
                search_text = search_text[:-1]
                search_bar_win.clear()
                search_bar_win.border(0)
                search_bar_win.addstr(1, 1, f"Search: {search_text}")
            elif key == ord('\n'):  # Enter to start search
                self.perform_search(menu_win, search_text, now_playing_win, recently_played_win)
                in_search = False
            elif 32 <= key < 127:  # Printable ASCII
                search_text += chr(key)
                search_bar_win.addstr(1, len(search_text) + 8, chr(key))
            else:
                # Handle media controls and other keys
                if key == ord('p'):  # Play/Pause
                    self.spotify.play_pause()
                elif key == ord('l'):  # Next track
                    self.spotify.next()
                elif key == ord('h'):  # Previous track
                    self.spotify.prev()

            search_bar_win.refresh()

    def perform_search(self, menu_win, search_text, now_playing_win, recently_played_win):
        """Perform search and display results."""
        search_results = self.search_instance.search(search_text)

        current_pos = 0
        while True:
            menu_win.clear()
            menu_win.border(0)
            menu_win.addstr(1, 1, "Search Results:")

            # Display search results
            for idx, track in enumerate(search_results["spotify"], 1):
                text = f"{idx}. {track['name']} by {track['artists'][0]['name']}"
                if idx - 1 == current_pos:
                    menu_win.addstr(2 + idx, 1, f"> {text}", curses.A_REVERSE)
                else:
                    menu_win.addstr(2 + idx, 1, text)

            menu_win.refresh()

            key = self.stdscr.getch()

            if key == ord('q'):  # Quit back to main menu
                break
            elif key in [curses.KEY_DOWN, ord('j')]:  # Navigate down
                current_pos = min(current_pos + 1, len(search_results["spotify"]) - 1)
            elif key in [curses.KEY_UP, ord('k')]:  # Navigate up
                current_pos = max(current_pos - 1, 0)
            elif key == ord('\n'):  # Enter to select track
                selected_track = search_results["spotify"][current_pos]
                self.spotify.play_track(selected_track['uri'])  # Play the selected track

                # Update 'Recently Played'
                self.recently_played_artists.append(selected_track['artists'][0]['name'])
                self.recently_played_artists = list(dict.fromkeys(self.recently_played_artists))  # Remove duplicates
                self.recently_played_artists = self.recently_played_artists[-10:]  # Keep only the last 10 artists

                # Write back to 'recent.txt'
                with open("recent.txt", "w") as f:
                    for artist in self.recently_played_artists:
                        f.write(artist + "\n")
                break

        # Return to the main menu to continue navigating
        self.navigate_menu()
