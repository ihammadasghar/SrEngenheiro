from controllers import FeatureController as fclr


async def main(message, features, records):
    if message.content.startswith("sr!"):
        commands = fclr.get_Commands(message.content)
        command = commands[1].upper()

        #  Special feature cases
        if command == "HELP":  #  Case: Requires all feature list
            response = help(features)
            await message.channel.send(response)
            return

        for feature in features:
            if command == feature.command:
                params = fclr.get_Args(commands, feature, records, message)
                if params is None:
                    await message.channel.send(f"{feature.command} requires {feature.nargs} arguments.")
                    return

                response = feature.view_Function(*params)
                await message.channel.send(response)
                return

        await message.channel.send(f"Sorry, I dont understand this command :/")
        return


def greet(message):
    nickname = message.author.nick
    name = message.author.display_name
    if nickname == None:
        response = f"Hi {name}! `sr! help` to see how I can help"
    else:
        response = f"Hi {nickname}! `sr! help` to see how I can help"
    return response


def today():
    date_Today = fclr.get_Date_Today()
    response = f"Date today is `{date_Today}`"
    return response


def praise():
    response = "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧"
    return response


def scold():
    response = "ಥ_ಥ"
    return response


def notes(args, records):
    action =  args[0].upper()
    if action == "ADD":
        try:
            topic = args[1].upper()
            
            if type(args[2]) == list:
                entries = args[2]
                names = ""
                added = True
                for entry in entries:
                    name = entry[0].upper()
                    names += name + ", "
                    added = fclr.add_Note(records=records, topic=topic, name=name, item=entry[1])
                if added:
                    response = f"Noted {names} in topic {topic}."
                    return response
                response = f"One or more of notes {names} already exists in topic {topic}."
                return response

            name = args[2].upper()
            item = args[3].upper()
            added = fclr.add_Note(records=records, topic=topic, name=name, item=item)

            if added:
                response = f"Noted {name} in topic {topic}."
                return response
            response = f"A note with the name {name} already exists in topic {topic}."
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
    
    elif action == "EDIT":
        try:
            topic = args[1].upper()
            
            if type(args[2]) == list:
                entries = args[2]
                names = ""
                edited = True
                for entry in entries:
                    name = entry[0].upper()
                    names += name + ", "
                    edited = fclr.edit_Note(records=records, topic=topic, name=name, item=entry[1])
                if edited:
                    response = f"Noted {names} edited in topic {topic}."
                    return response
                response = f"One or more of notes {names} dont exist in topic {topic}."
                return response

            name = args[2].upper()
            item = args[3].upper()
            edited = fclr.edit_Note(records=records, topic=topic, name=name, item=item)

            if edited:
                response = f"Note {name} edited in topic {topic}."
                return response
            response = f"Note {name} doesn't exist in topic {topic}."
            return response

        except IndexError:
            print("arguments error raised")
            return "Missing arguments."
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
                added = True
                for entry in entries:
                    name = entry[0].upper()
                    names += name + ", "
                    added = fclr.add_Event(records=records, topic=topic, name=name, date=entry[1])
                if added:
                    response = f"Events {names} added in topic {topic}."
                    return response
                response = f"One or more of events {names} already exists in topic {topic}."
                return response

            name = args[2].upper()
            date = args[3].upper()
            added = fclr.add_Event(records=records, topic=topic, name=name, date=date)

            if added:
                response = f"Event {name} added in topic {topic}."
                return response
            response = f"Event {name} already exists in topic {topic}."
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
        
    elif action == "URGENT":
        if len(args) == 1:
            response = fclr.urgent_Events(records)
            if not response:
                response = "Nothing urgent, no events in the next 7 days."
            return response 
    
    elif action == "EDIT":
        try:
            topic = args[1].upper()
            
            if type(args[2]) == list:
                entries = args[2]
                names = ""
                edited = True
                for entry in entries:
                    name = entry[0].upper()
                    names += name + ", "
                    edited = fclr.add_Edit(records=records, topic=topic, name=name, date=entry[1])
                if edited:
                    response = f"Events {names} edited in topic {topic}."
                    return response
                response = f"One or more of events {names} don't exist in topic {topic}."
                return response

            name = args[2].upper()
            date = args[3].upper()
            edited = fclr.edit_Event(records=records, topic=topic, name=name, date=date)

            if edited:
                response = f"Event {name} edited in topic {topic}."
                return response
            response = f"Event {name} doesn't exist in topic {topic}."
            return response

        except IndexError:
            print("arguments error raised")
            return "Missing Arguments."

    else:
        return f"I don't know how to perform the action {action}."


def help(features):
    response = fclr.get_Commands_Description(features)
    return response
