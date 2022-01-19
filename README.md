# discord-drawbot version 2.0
***Made by drawbu***

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/95fca3eeb6184cd487b0bcca0bcd1d2e)](https://app.codacy.com/gh/drawbu/drawbot?utm_source=github.com&utm_medium=referral&utm_content=drawbu/drawbot&utm_campaign=Badge_Grade_Settings)
![GitHub](https://img.shields.io/github/license/drawbu/drawbot)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/drawbu/drawbot)
![GitHub repo size](https://img.shields.io/github/repo-size/drawbu/drawbot)
![Lines of code](https://img.shields.io/tokei/lines/github/drawbu/drawbot)
![GitHub last commit](https://img.shields.io/github/last-commit/drawbu/drawbot)
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/drawbu/drawbot)

A Pronote notifier discord bot.

Help server: https://discord.gg/XGXydQyKhQ

|  :bangbang:  | Don't try with a wrong username or password too many time, or you can get banned from Pronote                        |
|:------------:|:---------------------------------------------------------------------------------------------------------------------|
|  :warning:   | We do not take responsibility for a possible leak of your passwords, which is why you need to host the bot yourself. |

## Installation
```sh
git clone https://github.com/drawbu/drawbot

cd /path

pip install -r requirements.txt
```

## Launch
```sh
py run.py
```

## Files documentation

The bot will create **2** json files in the **app** folder:

-   config.json
-   devoirs.json

### app/ config.json

This file stocks your private logins and info's to make to bor running:

```json5
{
    "token": "( ͡° ͜ʖ ͡°)",
    "prefix": "!",
    "channelID": "000000000000000000",
    "username": "demonstration",
    "password": "pronotevs",
    "url": "https://demo.index-education.net/pronote/eleve.html?login=true"
}
```
THESE ARE JUST EXAMPLES

In `"token"`, you need to add your bot token. <br>
In `"prefix"`, the prefix your bot will use. <br>
In `"channelID"`, the ID of the Discord channel. <br>
In `"username"`, your Pronote username. <br>
In `"password"`, your Pronote password. <br>
In `"url"`, the url of your pronote client. <br>

If you can't connect to Pronote, check if your establishment is not using an 
ENT. In this case, see what you need to do with the help of the pronote wrapper 
project: [pronotepy](https://github.com/bain3/pronotepy)

### app/ devoirs.json
Automatically generated JSON containing homeworks information.
