# Linux Spoitfy TUI Front-end which doesn't require premium
This is a simple Python project which utilizes Spotipy (Spotify Python API) to control, search, and play songs from an existing Spotify client through a simple and clean terminal interface. While there already is applications that do so (Spotify-TUI comes to mind) these usually require Spotify Premium as they are standalone applications. This is not a standalone application and *WILL PLAY ADS* if spotify premium is not subscribed to by the active account. 
![image](https://github.com/RLB2310/SpotSonic/assets/107162850/24bd0667-6ce2-4438-a65e-2b5cb2eda53f)

* Terminal: Alacrity + Opacity Changes, Under Hyprland Arch

The Spotify API requires a dev app to be running (https://developer.spotify.com/documentation/web-api/concepts/apps) and assumes you set the SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET environment variables. 
Recently played artists are simply written to a ".txt" file and updated on search.
It is suggested to minimize or hide the actual Spotify application unless audio control is needed obviously.

*This is by no means a refined or professional application, just a cool idea, and will most likely break.*
