from controllers import FeatureController as fclr
from controllers import ValidationController as vclr
from controllers import PersistenceController as pclr


async def main(message, features, server):
    #  Getting server records
    records = await pclr.load_Records(server)
    
    if message.content.startswith("sr!"):
        commands = vclr.get_Commands(message.content)
        command = commands[1].upper()

        #  Special feature cases
        if command == "HELP":  #  Case: Requires all feature list
            response = help(features)
            await message.channel.send(response)
            return

        for feature in features:
            if command == feature.command:
                params = vclr.get_Args(commands, feature, records, message)
                response = feature.view_Function(*params)
                await message.channel.send(response)

                #  Update Records
                if records.updated:
                    await pclr.save_Records(records.records, server)
                
                # If user has requested to fetch a message
                id = records.requested_message_ID if records.requested_message_ID else None
                return id

        await message.channel.send(f"Sorry, I dont understand this command :/")
        return


def greet(message):
    name = message.author.display_name
    response = f"Hi {name}! `sr! help` to see how I can help"
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


def remember_Message(args, records, message):
    if len(args) != 1 or type(args[0]) == list:
        return "I don't understand :/\nCorrect command to remember:\n`sr! remember [name]`"
    
    if message.reference.message_id == None:
        return "You need to reply this command to the message I need to remember."

    name = args[0]
    added = fclr.add_Message(name, message.reference.message_id, records)
    if added:
        return f"I'll keep an eye on **{name}**"

    return f"A message with the name **{name}** already exists"


def get_Message(args, records):
    if len(args) != 1 or type(args[0]) == list:
        return "I don't understand :/\nCorrect command to get remembered message:\n`sr! get [name]`"
    
    name = args[0]
    found = fclr.get_Message(name, records)
    if found:
        return f"Remembering **{name}**..."

    return f"I don't remember the message **{name}**"


def forget_Message(args, records):
    if len(args) != 1:
        return "I don't understand :/\nCorrect command to forget:\n`sr! forget [name]`"
    
    name = args[0]
    deleted = fclr.delete_Message(name, records)
    if deleted:
        return f"**{name}** forgotten."

    return f"Couldn't find a message named **{name}**"


def notes(args, records):
    action =  args[0].upper()
    if action == "ADD":
        if len(args) != 4 and len(args) != 3:
            response = "I don't understand :/\nCorrect command to add note:\n`sr! notes add [topic] [name] [content]`"
            return response

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
                response = f"Noted **{names}** in topic **{topic}**."
                return response
            response = f"One or more of notes **{names}** already exists in topic **{topic}**."
            return response

        name = args[2].upper()
        item = args[3].upper()
        added = fclr.add_Note(records=records, topic=topic, name=name, item=item)

        if added:
            response = f"Noted **{name}** in topic **{topic}**."
            return response
        response = f"A note with the name **{name}** already exists in topic **{topic}**."
        return response


    elif action == "DELETE":
        if len(args) != 3 and len(args) != 2:
            response = "I don't understand :/\nCorrect command to delete note:\n`sr! notes delete [topic] [name(optional)]`"
            return response

        topic = args[1].upper()
        if len(args) == 3:
            name = args[2].upper()
            is_Deleted = fclr.delete_Note(topic=topic, name=name, records=records)
            if is_Deleted:
                response = f"Note **{name}** deleted from topic **{topic}**."
                return response

            response = f"Couldn't find note **{name}**."
            return response

        is_Deleted = fclr.delete_Notes_Topic(topic=topic, records=records)
        if is_Deleted:
                response = f"Notes topic **{topic}** deleted."
                return response
        response = f"Couldn't find notes topic **{topic}**."
        return response


    elif action == "GET":
        if len(args) != 3 and len(args) != 2 and len(args) != 1:
            response = "I don't understand :/\n Correct command to get note:\n`sr! notes get [topic] [name(optional)]`"
            return response

        #  Get note topic names
        if len(args) == 1:
            topic_names = fclr.get_Notes(records)
            if topic_names is None:
                return "There are no added notes."

            response = f"**Note topics:**\n"
            for name in topic_names:
                response += f"-> {name}\n"
            
            return response

        topic = args[1].upper()
        if len(args) == 3:
            name = args[2].upper()
            note = fclr.get_Note(topic=topic, name=name, records=records)
            if not note:
                return f"Couldn't find note **{name}**."
            return note

        topic_Notes = fclr.get_Notes_Topic(topic=topic, records=records)
        if not topic_Notes:
            return f"Couldn't find notes on topic **{topic}**."
        return topic_Notes


    elif action == "EDIT":
        if len(args) != 4 and len(args) != 3:
            response = "I don't understand :/\n Correct command to edit note:\n`sr! notes edit [topic] [name] [content]`"
            return response

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
                response = f"Noted **{names}** edited in topic **{topic}**."
                return response
            response = f"One or more of notes **{names}** dont exist in topic **{topic}**."
            return response

        name = args[2].upper()
        item = args[3].upper()
        edited = fclr.edit_Note(records=records, topic=topic, name=name, item=item)

        if edited:
            response = f"Note **{name}** edited in topic **{topic}**."
            return response
        response = f"Note **{name}** doesn't exist in topic **{topic}**."
        return response


    else:
        return f"I don't know how to perform the action **{action}**."


def events(args, records):
    if len(args) == 0:
        all_events = fclr.get_Ordered_Events(records)
        if all_events is None:
            return "There are no upcoming added events."

        response = "**Upcoming events:**\n"
        for event in all_events:
            response += f"-> **({event['Topic']})** {event['Name']} - `{event['Date']}`\n"
        return response

    action =  args[0].upper()
    if action == "ADD":
        if len(args) != 4 and len(args) != 3:
            response = "I don't understand :/\nCorrect command to add event:\n`sr! events add [topic] [name] [date]`"
            return response

        topic = args[1].upper()
        
        if type(args[2]) == list:
            entries = args[2]
            names = ""
            added = True
            for entry in entries:
                name = entry[0].upper()
                date = entry[1]
                if vclr.get_Days_Left(date) < 0:
                    return f"Event **{name}** date `{date}` has already passed.\nIf you still want me to remember it, add a note."

                names += name + ", "
                added = fclr.add_Event(records=records, topic=topic, name=name, date=entry[1])
            if added:
                response = f"Events **{names}** added in topic **{topic}**."
                return response
            response = f"One or more of events **{names}** already exists in topic **{topic}**."
            return response

        name = args[2].upper()
        date = args[3].upper()
        if vclr.get_Days_Left(date) < 0:
            return f"Event **{name}** date `{date}` has already passed.\nIf you still want me to remember it, add a note."
        added = fclr.add_Event(records=records, topic=topic, name=name, date=date)

        if added:
            response = f"Event **{name}** added in topic **{topic}**."
            return response
        response = f"Event **{name}** already exists in topic **{topic}**."
        return response


    elif action == "DELETE":
        if len(args) != 3 and len(args) != 2:
            response = "I don't understand :/\n Correct command to delete event:\n`sr! events delete [topic] [name(Optional)]`"
            return response

        topic = args[1].upper()
        if len(args) == 3:
            name = args[2].upper()
            is_Deleted = fclr.delete_Event(topic=topic, name=name, records=records)
            if is_Deleted:
                response = f"Event **{name}** deleted from topic **{topic}**."
                return response

            response = f"Couldn't find event **{name}**."
            return response

        is_Deleted = fclr.delete_Events_Topic(topic=topic, records=records)
        if is_Deleted:
                response = f"Events topic **{topic}** deleted."
                return response
        response = f"Couldn't find events topic **{topic}**."
        return response
    
    elif action == "GET":
        if len(args) != 3 and len(args) != 2 and len(args) != 1:
            response = "I don't understand :/\n Correct command to get event:\n`sr! events get [topic] [name(Optional)]`"
            return response

        #  Get note topic names
        if len(args) == 1:
            topic_names = fclr.get_Events(records)
            if topic_names is None:
                return "There are no added events."

            response = f"**Event topics:**\n"
            for name in topic_names:
                response += f"-> {name}\n"
            
            return response

        topic = args[1].upper()
        if len(args) == 3:
            name = args[2].upper()
            event = fclr.get_Event(topic=topic, name=name, records=records)
            if not event:
                return f"Couldn't find event **{name}**."
            return event

        topic_Events = fclr.get_Events_Topic(topic=topic, records=records)
        if not topic_Events:
            return f"Couldn't find events on topic **{topic}**."
        return topic_Events


    elif action == "URGENT":
        response = fclr.urgent_Events(records)
        if not response:
            response = "Nothing urgent, no events in the next 7 days."
        return response 
    

    elif action == "EDIT":
        if len(args) != 4 and len(args) != 3:
            response = "I don't understand :/\n Correct command to edit events:\n`sr! events edit [topic] [name] [date]`"
            return response

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
                response = f"Events **{names}** edited in topic **{topic}**."
                return response
            response = f"One or more of events **{names}** don't exist in topic **{topic}**."
            return response

        name = args[2].upper()
        date = args[3].upper()
        edited = fclr.edit_Event(records=records, topic=topic, name=name, date=date)

        if edited:
            response = f"Event **{name}** edited in topic **{topic}**."
            return response
        response = f"Event **{name}** doesn't exist in topic **{topic}**."
        return response

    else:
        return f"I don't know how to perform the action **{action}**."


def help(features):
    response = fclr.get_Commands_Description(features)
    return response
