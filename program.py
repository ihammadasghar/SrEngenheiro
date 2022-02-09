from controllers.FeatureController import FeatureController
from models.Server import Server
from models.Records import Records
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

        if message.content.startswith("sr!"):
            commands =  message.content.split(" ")
            command = commands[1]

            data_Channel = discord.utils.get(message.guild.channels, name="bot-data")
            if not data_Channel:
                await message.channel.send("Sorry, couldn't find bot-data channel.")
                return

            data_Messages = await data_Channel.history(limit=500).flatten()
            
            records = Records(data_Messages, data_Channel)
            server =  Server(records, data_Channel)

            feature_Controller = FeatureController(message, server)
            for feature in feature_Controller.features:
                if command == feature.command:
                    #  Arguments validations
                    if type(feature.args) == list:
                        if len(commands)-2 in feature.args:
                            arguments = [commands[i+2] for i in range(len(commands)-2)]
                    elif len(commands)-2 == feature.args: 
                        arguments = [commands[i+2] for i in range(len(commands)-2)]
                    else:
                        await message.channel.send(f"{feature.command} requires {feature.args} arguments.")
                        return

                    await feature.functionality(*arguments)
                    return

            await message.channel.send(f"Sorry, I dont understand")
            return

    bot.run(os.getenv("TOKEN"))