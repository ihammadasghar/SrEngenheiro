from email import message
from discord.utils import get


async def get_tag_data(guild_data, data_tag):
    for message in guild_data:
        if message.startswith(data_tag):
            return message 