from models.Records import Records
from models.Server import Server
from features_Config import features
from views.response import main
import pickle
from os import remove
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
        data_Messages = await data_Channel.history(limit=500).flatten()

        guild_ID = message.guild.id
        record_Message = None
        for m in data_Messages:
            if m.content.startswith(str(guild_ID)):
                record_Message = m

        server = Server(record_Message=record_Message, data_Channel=data_Channel, ID=guild_ID)
        records = await load_Records(server)
        records = Records(records, server)

        await main(message, features, records)

        if records.updated:
            await save_Records(records.records, server)

        if records.requested_message_ID:
            found = False
            r_message = None
            for channel in bot.get_guild(guild_ID).channels:
                if r_message:
                    break
                try:
                    r_message = await channel.fetch_message(id=records.requested_message_ID)
                except:
                    continue
            name = r_message.author.display_name

            content = f'**Remembered Message:**\n"{r_message.content}" - **By {name}**'
            await message.channel.send(content=content, files=r_message.attachments)
    
    async def load_Records(server):
        #  If record doesn't exist
        if not server.record_Message:
            await save_Records({}, server)
            return {}
        
        file = await server.record_Message.attachments[0].to_file()
        file = file.fp

        data = pickle.load(file)
        return data['Records']

    async def save_Records(records, server):
        if server.record_Message:
            await server.record_Message.delete()
        data = {"Server_ID": server.ID, "Records": records}

        filepath = f"./{server.ID}"
        with open(filepath, mode="wb") as file:
            pickle.dump(data, file)


        file = discord.File(filepath)
        await server.data_Channel.send(content=str(server.ID), file=file)
        remove(filepath)


    bot.run(os.getenv("TOKEN"))