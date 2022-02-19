from controllers import FeatureController as fclr
from controllers import ValidationController as vclr
from controllers import PersistenceController as pclr
from settings import ALLOWED_NOTE_CHARACTERS

async def main(message, features, server):
    #  Getting server records
    records = await pclr.load_Records(server)
    
    commands = vclr.get_Commands(message.content)
    command = commands[1].upper()

    #  Special feature cases
    if command == "HELP":  #  Case: Requires all feature list
        response = help(features)
        await message.channel.send(response)
        return

    #  Identify feature to execute
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
    return f"Hi {name}! `sr! help` to see how I can help"


def today():
    date_Today = fclr.get_Date_Today()
    return f"Date today is `{date_Today}`"

#  Easter Egg
def praise():
    return "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧"

#  Easter Egg
def scold():
    return "ಥ_ಥ"

#  Remembering messages features
def remember_Message(args, records, message):
    #  Argument Validations
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
    #  Argument Validation
    if len(args) != 1 or type(args[0]) == list:
        return "I don't understand :/\nCorrect command to get remembered message:\n`sr! get [name]`"
    
    name = args[0]
    found = fclr.get_Message(name, records)
    if found:
        return f"Searching through memories for **{name}**..."

    return f"I don't remember the message **{name}**"


def forget_Message(args, records):
    #  Argument Validation
    if len(args) != 1:
        return "I don't understand :/\nCorrect command to forget:\n`sr! forget [name]`"
    
    name = args[0]
    deleted = fclr.delete_Message(name, records)
    if deleted:
        return f"**{name}** forgotten."

    return f"Couldn't find a message named **{name}**"


def notes(args, records):
    #  Topic names
    if len(args) == 0:
        topic_names = fclr.get_Notes(records)
        if topic_names is None:
            return "There are no added notes."

        response = f"**Note topics:**\n"
        for name in topic_names:
            response += f"-> {name}\n"
        
        return response

    action =  args[0].upper()
    if action == "ADD":
        #  Argument Validations
        if len(args) != 4 and len(args) != 3:
            return "I don't understand :/\nCorrect command to add note:\n`sr! notes add [topic] [name] [content]`"

        topic = args[1].upper()
        
        #  Multiple note entries
        if type(args[2]) == list:
            entries = args[2]
            names = ""
            added = True
            for entry in entries:
                name = entry[0].upper()
                names += name + ", "
                item = entry[1]
                if not len(item)<=ALLOWED_NOTE_CHARACTERS and len(item)>0:
                    return f"Note {name} should be less than 240 characters"
                added = fclr.add_Note(records=records, topic=topic, name=name, item=item)

            if added:
                return f"Noted **{names}** in topic **{topic}**."

            return f"One or more of notes **{names}** already exists in topic **{topic}**."

        #  Single note entry
        name = args[2].upper()
        item = args[3].upper()
        if not len(item)<=ALLOWED_NOTE_CHARACTERS and len(item)>0:
            return "Notes should be less than 240 characters"

        added = fclr.add_Note(records=records, topic=topic, name=name, item=item)

        if added:
            return f"Noted **{name}** in topic **{topic}**."

        return f"A note with the name **{name}** already exists in topic **{topic}**."


    elif action == "DELETE":
        # Argument Validations
        if len(args) != 3 and len(args) != 2:
            response = "I don't understand :/\nCorrect command to delete note:\n`sr! notes delete [topic] [name(optional)]`"
            return response

        topic = args[1].upper()
        if len(args) == 3:
            name = args[2].upper()
            deleted = fclr.delete_Note(topic=topic, name=name, records=records)
            if deleted:
                return f"Note **{name}** deleted from topic **{topic}**."

            return f"Couldn't find note **{name}**."

        deleted = fclr.delete_Notes_Topic(topic=topic, records=records)
        if deleted:
                response = f"Notes topic **{topic}** deleted."
                return response
        response = f"Couldn't find notes topic **{topic}**."
        return response


    elif action == "GET":
        #  Argument Validations
        if len(args) != 3 and len(args) != 2 and len(args) != 1:
            response = "I don't understand :/\n Correct command to get note:\n`sr! notes get [topic] [name(optional)]`"
            return response

        #  Single Note
        topic = args[1].upper()
        if len(args) == 3:
            name = args[2].upper()
            note = fclr.get_Note(topic=topic, name=name, records=records)
            if not note:
                return f"Couldn't find note **{name}**."
            return note

        # Note topic
        topic_Notes = fclr.get_Notes_Topic(topic=topic, records=records)
        if not topic_Notes:
            return f"Couldn't find notes on topic **{topic}**."
        return topic_Notes


    elif action == "EDIT":
        #  Argument Validations
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
    # Listing Ordered Events
    #  Argument Validations
    if len(args) == 0:
        all_events = fclr.get_Ordered_Events(records)
        if all_events is None:
            return "There are no upcoming added events."

        response = "**Upcoming events:**\n"
        for event in all_events:
            response += f"-> `{event['Date']}` - **({event['Topic']})** {event['Name']}\n"
        return response

    # CRUD Actions
    action =  args[0].upper()
    if action == "ADD":
        #  Argument Validations
        if len(args) != 4 and len(args) != 3:
            response = "I don't understand :/\nCorrect command to add event:\n`sr! events add [topic] [name] [date]`"
            return response

        # Multiple events
        topic = args[1].upper()
        if type(args[2]) == list:
            entries = args[2]
            names = ""
            added = True
            for entry in entries:
                name = entry[0].upper()
                date = entry[1]
                if vclr.to_Date(date) == False:
                    return f"On event {name} date format should be Day/Month/Year"

                if vclr.get_Days_Left(date) < 0:
                    return f"Event **{name}** date `{date}` has already passed.\nIf you still want me to remember it, add a note."

                names += name + ", "
                added = fclr.add_Event(records=records, topic=topic, name=name, date=entry[1])

            if added:
                response = f"Events **{names}** added in topic **{topic}**."
                return response

            response = f"One or more of events **{names}** already exists in topic **{topic}**."
            return response

        #  Single event
        name = args[2].upper()
        date = args[3].upper()
        if vclr.to_Date(date) == False:
            return "Date format should be Day/Month/Year"

        if vclr.get_Days_Left(date) < 0:
            return f"Event **{name}** date `{date}` has already passed.\nIf you still want me to remember it, add a note."

        added = fclr.add_Event(records=records, topic=topic, name=name, date=date)
        if added:
            response = f"Event **{name}** added in topic **{topic}**."
            return response
        response = f"Event **{name}** already exists in topic **{topic}**."
        return response


    elif action == "DELETE":
        #  Argument Validations
        if len(args) != 3 and len(args) != 2:
            response = "I don't understand :/\n Correct command to delete event:\n`sr! events delete [topic] [name(Optional)]`"
            return response

        topic = args[1].upper()
        #  Argument Validations
        if len(args) == 3:
            name = args[2].upper()
            deleted = fclr.delete_Event(topic=topic, name=name, records=records)
            if deleted:
                response = f"Event **{name}** deleted from topic **{topic}**."
                return response

            response = f"Couldn't find event **{name}**."
            return response

        deleted = fclr.delete_Events_Topic(topic=topic, records=records)
        if deleted:
                response = f"Events topic **{topic}** deleted."
                return response
        response = f"Couldn't find events topic **{topic}**."
        return response
    
    elif action == "GET":
        #  Argument Validations
        if len(args) != 3 and len(args) != 2 and len(args) != 1:
            response = "I don't understand :/\n Correct command to get event:\n`sr! events get [topic] [name(Optional)]`"
            return response

        # Get specific event
        topic = args[1].upper()
        if len(args) == 3:
            name = args[2].upper()
            event = fclr.get_Event(topic=topic, name=name, records=records)
            if not event:
                return f"Couldn't find event **{name}**."

            text = f"**Event on topic {topic}:\n-> {name}** `{event}`"
            return text

        topic_Events = fclr.get_Events_Topic(topic=topic, records=records)
        if not topic_Events:
            return f"Couldn't find events on topic **{topic}**."
        return topic_Events

    elif action == "URGENT":
        response = fclr.urgent_Events(records)
        if not response:
            response = "Nothing urgent, no events in the next 7 days."
        return response

    elif action == "TOPICS":
        #  Get event topic names
        topic_names = fclr.get_Events(records)
        if topic_names is None:
            return "There are no added events."

        response = f"**Event topics:**\n"
        for name in topic_names:
            response += f"-> {name}\n"
        
        return response
    

    elif action == "EDIT":
        #  Argument Validations
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
