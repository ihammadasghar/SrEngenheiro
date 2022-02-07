from controllers.FeatureController import get_Features
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

            channel = discord.utils.get(message.guild.channels, name="bot-data")
            if not channel:
                await message.channel.send("Sorry, couldn't find bot-data channel.")
                return

            guild_data = channel.history(limit=500)

            features = get_Features()
            for feature in features:
                if command == feature.command:
                    if len(commands)-2 == feature.args:
                        arguments = [commands[i+2] for i in range(len(commands)-2)]
                        
                        if feature.data_required:
                            await feature.functionality(*arguments, message=message, data=guild_data)
                            return
                        await feature.functionality(*arguments, message=message)
                        return

                    await message.channel.send(f"{feature.command} requires {feature.args} arguments.")
                    return
                    
            await message.channel.send(f"Sorry, I dont understand")
            return

    bot.run(os.getenv("TOKEN"))