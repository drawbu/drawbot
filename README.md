# discord-drawbot version 1.1
***Made by drawbu***

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/95fca3eeb6184cd487b0bcca0bcd1d2e)](https://app.codacy.com/gh/drawbu/drawbot?utm_source=github.com&utm_medium=referral&utm_content=drawbu/drawbot&utm_campaign=Badge_Grade_Settings)
![GitHub](https://img.shields.io/github/license/drawbu/drawbot)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/drawbu/drawbot)
![GitHub repo size](https://img.shields.io/github/repo-size/drawbu/drawbot)
![Lines of code](https://img.shields.io/tokei/lines/github/drawbu/drawbot)
![GitHub last commit](https://img.shields.io/github/last-commit/drawbu/drawbot)
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/drawbu/drawbot)

A Pronote notifier discord bot.

:bangbang: | don't try with a wrong username or password too many time, or you can get banned from Pronote
:---: | :---
:warning: | at the first launch, it might send a lot of messages


## Installation
```sh
- git clone https://github.com/drawbu/drawbot

- cd /path

- pip install -r requirements.txt
```


## files documentation

On first start, the bot will create **3** json files :

-   config.json
-   devoirs.json
-   pronote.json

### config.json

This file stocks your bot's **token** and **prefix** like this:

```json5
{
    "token": "( ͡° ͜ʖ ͡°)", // bot token
    "prefix": "!" // bot prefix
}
```

In `token`, you need to add your bot's token.
In `prefix`, the prefix your bot's will use without and restart.
It's the only file that you need to change to run the bot by your own.

### pronote.json

You pronote credentials.

```json5
{
    "username": null,  // Pronote username
    "password": null,  // Pronote password
    "channelID": null, // Channel to send homeworks
    "url": null // School pronote url
}
```

### devoirs.json
Automatically generated JSON containing homeworks information.

*Do not modify*
