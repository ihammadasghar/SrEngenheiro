from models.Feature import Feature


def get_Features():
    #  Intialize your feature here
    greeting = Feature("greet", 0, greet)
    gethelp =  Feature("!gethelp", 1, get_Help)
    addevent = Feature("addevent",2,add_event)
    #  Add the initialized feature here
    features = [greeting, gethelp, addevent]

    return features


async def greet(message):
    await message.channel.send(f"Hi {message.author}! I am Sr.Engenheiro\nWould you like some assistance today?")
    return


async def get_Help(message):
    return

async def add_event(event_name, event_date, message):
    events = {}
    events[event_name] = event_date
    await message.channel.send(f"I'll add it to the list.")
    return
