from models.Feature import Feature


def get_Features():
    #  Intialize your feature here
    greeting_feature =  Feature(command="greet", 
                                args=0, 
                                functionality=greet, 
                                description="greet: Be nice and say Hi to Sr.Engenheiro. :)"
                                )

    get_help_feature =  Feature(command="help", 
                                args=0, 
                                functionality=get_help,
                                description="help: Lists all commands."
                                )

    add_event_feature = Feature(command="addevent", 
                                args=2, 
                                functionality=add_event, 
                                data_required=True,
                                description="addevent eventname date: Adds an even to the calendar."
                                )

    #  Add the initialized feature here
    features = [greeting_feature, get_help_feature, add_event_feature]

    return features


async def greet(message):
    await message.channel.send(f"Hi {message.author}! I am Sr.Engenheiro\nWould you like some assistance today?")
    return


async def add_event(event_name, event_date, message, data):
    events = {}
    events[event_name] = event_date
    await message.channel.send(f"I'll add it to the list.")
    return


async def get_help(message):
    text = ""
    features = get_Features()
    for feature in features:
        text += feature.description + "\n"
    
    await message.channel.send(text)
    return
