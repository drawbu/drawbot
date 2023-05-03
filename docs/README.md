# discord-drawbot

**_Made by drawbu_**

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/95fca3eeb6184cd487b0bcca0bcd1d2e)](https://app.codacy.com/gh/drawbu/drawbot?utm_source=github.com&utm_medium=referral&utm_content=drawbu/drawbot&utm_campaign=Badge_Grade_Settings)
![GitHub](https://img.shields.io/github/license/drawbu/drawbot)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/drawbu/drawbot)
![GitHub repo size](https://img.shields.io/github/repo-size/drawbu/drawbot)
![Lines of code](https://img.shields.io/tokei/lines/github/drawbu/drawbot)
![GitHub last commit](https://img.shields.io/github/last-commit/drawbu/drawbot)
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/drawbu/drawbot)

A Pronote notifier discord bot.

We now have a Discord sever! You can join it if you have some questions,
some issues or just want to talk about the bot.
[Click here to join](https://discord.gg/XGXydQyKhQ)

| :bangbang: | Don't try with a wrong username or password too many time, or you can get banned from Pronote                            |
|:----------:|:-------------------------------------------------------------------------------------------------------------------------|
| :warning:  | We do not take responsibility for a possible leak of your passwords, which is why **you need to host the bot yourself.** |

## Some screenshots

![Homework message](assets/homework-message.png)
![Grade message](assets/grade-message.png)

## Installation

```sh
git clone https://github.com/drawbu/drawbot
cd drawbot

pip install -e .
```

## Launch

```sh
py drawbot
```

_If you are using a Linux distribution or macOS, you can use the `make` command to install dependencies and run the bot._

## Files documentation

The bot will create **3** json files in the **vars** folder:

- devoirs.json
- grades.json
- config.json

### vars/config.json

This file stocks your private logins and info's to make to bot running.
You can find a **config.example.json** file in the **vars** folder.

> `config.json` **Example**

```json5
{
    token: "( ͡° ͜ʖ ͡°)",
    channelID: "000000000000000000",
    username: "demonstration",
    password: "pronotevs",
    url: "https://demo.index-education.net/pronote/eleve.html?login=true",
    ping: "<@000000000000000000>"
}
```

copy that file as **config.json** and fill in the values as follows:

- `"token"`: your bot token. <br>
- `"channelID"`: the ID of the Discord channel. <br>
- `"username"`: your Pronote username. <br>
- `"password"`: your Pronote password. <br>
- `"url"`: the url of your pronote client. <br>
- `"ping"`: the ping you want to send with the message.
  It can be a discord user, a role, multiple mentions...
  Note that mentions should keep discord mentions style
  (`<@user_id>` or/and `<@&role_id>`) <br>

If you can't connect to Pronote, check if your establishment is not using an
ENT. In this case, see what you need to do with the help of the pronote wrapper
project: [pronotepy](https://github.com/bain3/pronotepy)

Files `vars/devoirs.json` and `vars/grades.json` are here to stock what's has
been already sent, so you don't need to care about them


## Docker

You can also run the bot in a docker container.

You still need to clone the repository, and fill the `config.json` file.

Then, you can build the image:
```sh
docker build -t drawbot .
```

And run it:
```sh
docker run -d -it --rm drawbot
```
