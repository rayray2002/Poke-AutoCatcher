# Poke-AutoCatcher

A auto catcher and wondertrader for Discord bot Poké Catcher.

## How to Use?
1. Download Chromedriver for your Chrome version [here](https://chromedriver.chromium.org/).
2. Run catcher.exe or trader.exe.
3. Login your Discord account.
4. Enjoy auto catching and wondertrading.

## Config Setting
```angular2html
[default]
# Chromedriver path
driver_path = ./chromedriver

# Run channel
server_url = https://discord.com/channels/878300201541062656/878302161749033021
channel = 正義魔人的頻道

# Enable auto login
auto_login = 0
email =
password =

[catcher]
# Time to run
run_minutes = 15,45

# Bag ball lower limit
poke_ball = 10
great_ball = 10
ultra_ball = 10
master_ball = 1

[trader]
# Desire Pokemons
dream = Riolu

# Lowest CP interested in
CP = 2000
```