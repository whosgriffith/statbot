# Statbot
### Requirements

- pipenv
- Python (3.8 or higher)
- Postgres compatible database
- Discord application

### Required environment variables
Setup the following environment variables before runing the bot
- DISCORD_TOKEN (Bot token from discord developer portal)
- DB_USER
- DB_PASSWORD
- DB_NAME
- DB_HOST
- DB_PORT

### Local setup

Run the following commands

1. `pipenv install`
2. `pipenv shell`
3. `python main.py` to run the bot

### Commands
Always use `.statbot` before any command
1. **ranks** (Voice channels usage ranked by user)
2. **afk** (AFK channel usage by user)
3. **channels** (Voice channels usage)
4. **user @user** (User stats use)

Made with [Discord.py](https://github.com/Rapptz/discord.py/tree/v1.7.3)
