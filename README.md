# Linux Spotify TUI Front-end which doesn't require premium
This is a simple Python project which utilizes Spotipy (Spotify Python API) to control, search, and play songs from an existing Spotify client through a simple and clean terminal interface. While there already is applications that do so (Spotify-TUI comes to mind) these usually require Spotify Premium as they are standalone applications. This is not a standalone application and *!!! WILL PLAY ADS !!!!* if spotify premium is not subscribed to by the active account. 
![image](https://github.com/RLB2310/SpotSonic/assets/107162850/24bd0667-6ce2-4438-a65e-2b5cb2eda53f)

* Terminal: Alacrity + Opacity Changes, Under Hyprland Arch

# HOW TO RUN
Clone/Download files, run the "app.py" with python3.

# Controls

"S" to enter search

"ESC" to exit sub menu

Arrow keys to navigate

# Prerequisites

The Spotify API requires a dev app to be running (https://developer.spotify.com/documentation/web-api/concepts/apps) and assumes you set the SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET environment variables. 



Support for client credentials flow. Please follow these steps:

Register app: https://developer.spotify.com/my-applications/#!/applications
Edit your ~/.bashrc to export following values:

    export SPOTIPY_CLIENT_ID='your-spotify-client-id'

    export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'

Recently played artists are simply written to a ".txt" file and updated on search.
It is suggested to minimize or hide the actual Spotify application unless audio control is needed obviously.

# Disclaimer
* THIS SOFTWARE DOESN'T ALTER SPOTIFY *
* This is by no means a refined or professional application, just a cool idea, and will most likely break. This isn't meant to be applied to different setups and hardware, it probably won't work under most circumstances, and I don't plan on changing it. Feel free to make changes by all means. *
