from pyexpat import features
from models.Feature import Feature


def get_Features():
    #  Intialize your feature here
    greeting = Feature("greet", 0, greet)
    get_help =  Feature("help", 0, get_help_feature)
    
    #  Add the initialized feature here
    features = [greeting, get_help]

    return features


async def greet(message):
    await message.channel.send(f"Hi {message.author}! I am Sr.Engenheiro\nWould you like some assistance today?")
    return


async def get_help_feature(message):
    await message.channel.send(f"Here's a list of all the commands!!\n greet- Be nice and say Hi to Sr.Engenheiro. :)\n help- A list of all the commands.")
    
    return