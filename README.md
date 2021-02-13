# siegeStatsGrabber

Note: This only checks stats for players who play on PC, if you want me to add console support then let me know!

### What is this?
This is a small little script which fetches data from the Ubisoft API and prints certain statistics about a player to the terminal window.

```
Enter a username to search: beaulo.tsm
+-----------------------+-----------------+
| Username              | beaulo.tsm      |
| Ranked KD             | 1.33            |
| Ranked WL             | 2.57            |
| Ranked MATCHES PLAYED | 246             |
| Ranked RANK           | CHAMPION        |
| Ranked MMR            | 5792            |
| Ranked MAX MMR        | 5985 : CHAMPION |
| Ranked LAST MMR DIFF  | -49             |
| Ranked MAIN MAP       | VILLA : 1.31    |
| General ATK MAIN      | Zofia : 1.22    |
| General DEF MAIN      | Melusi : 1.42   |
+-----------------------+-----------------+
```

**Features:**
- See a players ranked statistics such as KD, winloss, number of matches played, rank, mmr and max mmr
- Check a players most played map, and their KD on it
- Get info on a players most played attacker and defender, along with their KD with them
- Search for multiple players at once (comma seperate them e.g. player1, player2, player3)
- Player info is cached in a text file, so the userId does not need to be retrieved everytime a request is made for the same player
- You can enter `t` as a username and if you return to the Rainbow Six Siege window and open your leaderboard for 5 seconds, then a screenshot of your leaderboard will be displayed (currently only works on 1080x1920), making it easier for you to check the stats of players in your lobby


Please note all information is gathered from the official Ubisoft API, if there are any issues with the information, bring it up with Ubisoft and not me.

### How did I get this information?
The API endpoints are easily gathered from checking which outbound requests are being sent to fetch JSON data on the official ubisoft stat tracking website at: [https://www.ubisoft.com/en-gb/game/rainbow-six/siege/stats/summary](https://www.ubisoft.com/en-gb/game/rainbow-six/siege/stats/summary "https://www.ubisoft.com/en-gb/game/rainbow-six/siege/stats/summary").

I figured out that the token parameter to fetch crutial information, such as session information, is simply comprised of a Ubisoft account email and password joined together and encoded with base64. The appId in the program can be anything, it really does not matter.

### What do I need to get started?
You will need:
- a Ubisoft account which does not have 2FA enabled (this is important), this is so the proper authorization tokens can be created and accepted to fetch the data

### How to run the script

1. Make sure you have `python 3.7+` installed, otherwise this script will not function as intended as certain features are used which are only available in 3.7 and above, e.g. f-strings
2. Clone this repo into a folder/directory which you would like to keep it in
3. Once you are inside the folder, run `pip install -r requirements.txt` to install all the dependencies for this script. If that fails to work then try `python -m pip install -r requirements.txt`
4. Now you need to add your ubisoft account email address and password, there are two ways of doing this:
[+] You can either set your email and password as enviromental variables under `email` and `email_password` respectively
[+] Or you can edit the Auth arguments to your email and password inside the run function, ln 254
5. Now you can simply call the script using `python getStats.py`


------------

If you have any suggestions, improvements or bugs then feel free to open up a pull-request with your thoughts! 💖
