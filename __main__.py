import logging
import os
import datetime

import discord
import PloudosAPI
# PloudOS has terminated their services

##################### BOT CONFIG #####################

PLOUDOS_USERNAME = ""
PLOUDOS_PASSWORD = ""
PLOUDOS_SERVER_INDEX = 1
DISCORD_BOT_TOKEN = ""
##################### BOT CONFIG #####################

log_directory_name= "logs"
os.makedirs(log_directory_name, exist_ok=True)

date = datetime.datetime.now()
log_time = f"{date.year}_{date.month}_{date.day}_{date.hour}:{date.minute}:{date.second}"

logging.basicConfig(level=logging.DEBUG, filename=f'./{log_directory_name}/{log_time}.txt')

client = discord.Client(intents=discord.Intents.all())


def log(message, level="info"):
    print(f"{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {level.upper()} {message}")
    if level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)
    elif level == "critical":
        logging.critical(message)

@client.event
async def on_ready():
    log(f"Bot started...")

@client.event
async def on_message(message):
    if message.author.bot: # Check if the message author is not a bot
        return
    
    if message.content.startswith('!startserver'):
        log(message.content)
        await start_ploudos_server(message)


async def start_ploudos_server(message):
    try:
        session = PloudosAPI.login(PLOUDOS_USERNAME, PLOUDOS_PASSWORD)
        server = session.get_server(PLOUDOS_SERVER_INDEX)
    except Exception as e:
        log(str(e), "critical")
        try:
            await message.channel.send("Failed to connect to PloudOS.")
        except Exception as e:
            log(str(e), "critical")
            log("Cant send a message to Discord. Probably internet is not available.", "critical")
        return
    
    await message.channel.send("Server is preparing...")

    try:
        result = server.start()
        log(result)
    except Exception as e:
        log(str(e), level="critical")
        await message.channel.send("The server did not boot for an unknown reason...")
        return

    log(f"{server.serverName} named server is starting... Called by: {message.author}")

    await message.channel.send("Server is starting...")
    log(f"Server: {server.serverName}")


client.run(DISCORD_BOT_TOKEN)
