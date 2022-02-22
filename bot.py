from models.Server import Server
from features_Config import features
from views.response import main
from settings import *
import discord


if __name__ == "__main__":
    bot = discord.Client()

    @bot.event
    async def on_ready():
        print(STARTUP_MESSAGE)

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        if message.content.startswith(ACTIVATION_SYMBOL):
            data_Channel = bot.get_channel(id=DATA_CHANNEL_ID)
            data_files = await data_Channel.history(limit=MAX_RECORD_FILES).flatten()

            guild_ID = message.guild.id
            record_file = None
            for file in data_files:
                if file.content.startswith(str(guild_ID)):
                    record_file = file

            server = Server(record_Message=record_file, data_Channel=data_Channel, ID=guild_ID)
            
            await main(message, features, server)


    bot.run(TOKEN)