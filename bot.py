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

        if message.content.startswith(ACTIVATION_WORD):
            data_Channel = bot.get_channel(id=DATA_CHANNEL_ID)
            data_files = await data_Channel.history(limit=MAX_RECORD_FILES).flatten()

            guild_ID = message.guild.id
            record_file = None
            for file in data_files:
                if file.content.startswith(str(guild_ID)):
                    record_file = file

            server = Server(record_Message=record_file, data_Channel=data_Channel, ID=guild_ID)
            
            #  Find and send requested message
            requested_message_ID = await main(message, features, server)
            if requested_message_ID:
                r_message = None
                for channel in bot.get_guild(guild_ID).channels:
                    if r_message:
                        break
                    try:
                        r_message = await channel.fetch_message(id=requested_message_ID)
                    except:
                        continue
                name = r_message.author.display_name

                content = f'**Remembered Message:**\n"{r_message.content}" - **By {name}**'
                await message.channel.send(content=content, files=r_message.attachments)


    bot.run(TOKEN)