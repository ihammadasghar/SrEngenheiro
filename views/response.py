from controllers import FeatureController as fclr


async def main(message, features, records):
    if message.content.startswith("sr!"):
        parts = message.content.split("\n")
        commands =  parts[0].split(" ")

        if len(commands) < 2:
            response = help(features)
            await message.channel.send(response)
            return
        
        if len(parts) > 1:
            items = []
            for item in parts[1:]:
                items.append(item.split(" "))
            commands.append(items)

        command = commands[1].upper()

        #  Special feature cases
        if command == "HELP":  #  Case: Requires all feature list
            response = help(features)
            await message.channel.send(response)
            return

        for feature in features:
            if command == feature.command:
                #  Arguments validations
                if type(feature.nargs) == list:
                    if len(commands)-2 in feature.nargs:
                        arguments = [commands[i+2] for i in range(len(commands)-2)]
                elif len(commands)-2 == feature.nargs: 
                    arguments = [commands[i+2] for i in range(len(commands)-2)]
                else:
                    await message.channel.send(f"{feature.command} requires {feature.nargs} arguments.")
                    return

                try:
                    params = []
                    if not feature.nargs == 0:
                        params.append(arguments)

                    if feature.records_Required:
                        params.append(records)

                    if feature.message_Required:
                        params.append(message)

                    response = feature.view_Function(*params)
                    await message.channel.send(response)
                    return

                except:
                    await message.channel.send(f"Sorry, something went wrong :(")
                return

        await message.channel.send(f"Sorry, I dont understand this command :/")
        return


def greet(message):
    response = f"Hi {message.author.nick}! Sr.Engenheiro here\n-> 'sr! help' to see how I can help"
    return response


def today():
    date_Today = fclr.get_Date_Today()
    response = f"Date today is {date_Today}"
    return response


def praise():
    return "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧"


def events(args):
    pass


def notes(args, records):
    action =  args[0].upper()
    if action == "ADD":
        try:
            topic = args[1].upper()
            
            if type(args[2]) == list:
                entries = args[2]
                names = ""
                for entry in entries:
                    names += entry[0] + " "
                    fclr.add_Note(records=records, topic=topic, name=entry[0], item=entry[1])

                response = f"Noted {names} in topic {topic}."
                return response

            name = args[2].upper()
            item = args[3].upper()
            fclr.add_Note(records=records, topic=topic, name=name, item=item)

            response = f"Noted {name} in topic {topic}."
            return response

        except IndexError:
            print("arguments error raised")
            return "Missing arguments."


    elif action == "DELETE":
        topic = args[1].upper()
        if len(args) == 3:
            name = args[2].upper()
            is_Deleted = fclr.delete_Note(topic=topic, name=name, records=records)
            if is_Deleted:
                response = f"Note {name} deleted from topic {topic}."
                return response

            response = f"Couldn't find note {name}."
            return response

        is_Deleted = fclr.delete_Notes_Topic(topic=topic, records=records)
        if is_Deleted:
                response = f"Notes topic {topic} deleted."
                return response
        response = f"Couldn't find notes topic {topic}."
        return response
    
    elif action == "GET":
        topic = args[1].upper()
        if len(args) == 3:
            name = args[2].upper()
            note = fclr.get_Note(topic=topic, name=name, records=records)
            if not note:
                return f"Couldn't find note {name}."
            return note

        topic_Notes = fclr.get_Notes_Topic(topic=topic, records=records)
        if not topic_Notes:
            return f"Couldn't find notes on topic {topic}."
        return topic_Notes
        
    else:
        return f"I don't know how to perform the action {action}."


def events(args, records):
    action =  args[0].upper()
    if action == "ADD":
        try:
            topic = args[1].upper()
            
            if type(args[2]) == list:
                entries = args[2]
                names = ""
                for entry in entries:
                    names += entry[0] + " "
                    fclr.add_Event(records=records, topic=topic, name=entry[0], date=entry[1])

                response = f"Events {names} added in topic {topic}."
                return response

            name = args[2].upper()
            date = args[3].upper()
            fclr.add_Event(records=records, topic=topic, name=name, date=date)

            response = f"Event {name} added in topic {topic}."
            return response

        except IndexError:
            print("arguments error raised")
            return "Missing Arguments."


    elif action == "DELETE":
        topic = args[1].upper()
        if len(args) == 3:
            name = args[2].upper()
            is_Deleted = fclr.delete_Event(topic=topic, name=name, records=records)
            if is_Deleted:
                response = f"Event {name} deleted from topic {topic}."
                return response

            response = f"Couldn't find event {name}."
            return response

        is_Deleted = fclr.delete_Events_Topic(topic=topic, records=records)
        if is_Deleted:
                response = f"Events topic {topic} deleted."
                return response
        response = f"Couldn't find events topic {topic}."
        return response
    
    elif action == "GET":
        topic = args[1].upper()
        if len(args) == 3:
            name = args[2].upper()
            event = fclr.get_Event(topic=topic, name=name, records=records)
            if not event:
                return f"Couldn't find event {name}."
            return event

        topic_Events = fclr.get_Events_Topic(topic=topic, records=records)
        if not topic_Events:
            return f"Couldn't find events on topic {topic}."
        return topic_Events
        
    else:
        return f"I don't know how to perform the action {action}."


def help(features):
    response = fclr.get_Commands_Description(features)
    return response