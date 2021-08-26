# Poke-AutoCatcher

A auto catcher and wondertrader for Discord bot [Poké Catcher](https://top.gg/bot/707333868713410682).

## How to Use?
1. Download executable exe files in [release](https://github.com/rayray2002/Poke-AutoCatcher/releases).
2. Download Chromedriver for your Chrome version [here](https://chromedriver.chromium.org/). ([How to check your Chrome version](https://www.google.com/chrome/update/))
3. Run catcher.exe or trader.exe.
4. Login your Discord account.
5. Enjoy auto catching and wondertrading.

## Config Setting
```angular2html
[default]
# Chromedriver path
driver_path = ./chromedriver

# Run channel
server_url = https://discord.com/channels/878300201541062656/878302161749033021
channel = 正義魔人的頻道

# Enable auto login
auto_login = 0 # 1 for auto login
email = # email here
password = # password here

[catcher]
# Time to run
run_minutes = 15,45 # Runs at 8:15, 8:45, 9:15...

# Bag ball lower limit
poke_ball = 10
great_ball = 10
ultra_ball = 10
master_ball = 1

[trader]
# Desire Pokemons
dream = Riolu,Kubfu # Separate with , with no spaces

# Lowest CP interested in
CP = 2000
```