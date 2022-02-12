from pyexpat import features
from models.Records import Records
from feature_registry import features
from views.response import main
import discord
import os
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()

    bot = discord.Client()

    @bot.event
    async def on_ready():
        print("No Fear! Sr.Engenheiro here!")

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        data_Channel = bot.get_channel(id=941397535594008587)
        if not data_Channel:
            await message.channel.send("Sorry, I am having problems fetching data.")
            return

        data_Messages = await data_Channel.history(limit=500).flatten()

        records = Records(data_Messages, data_Channel, "941397423283134528")
        await main(message, features, records)
        

    bot.run(os.getenv("TOKEN"))