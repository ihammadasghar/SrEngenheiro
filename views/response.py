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


def help(features):
    descriptions = fclr.get_Commands_Description(features)
    response = "**Commands**\n"
    for description in descriptions:
        response += description + "\n"
    return response


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


def get(args, records):
    action =  args[0].lower()
    if action in ["note", "event"]:
        #  Argument Validations
        if len(args) != 3 and len(args) != 2 and len(args) != 1:
            response = f"I don't understand :/\n Correct command to get {action}:\n`sr!get {action} [topic] [name(optional)]`"
            return response

        #  Single item
        topic = args[1].upper()
        if len(args) == 3:
            name = args[2].upper()
            if action == "note":
                item = fclr.get_Note(topic=topic, name=name, records=records)
            else:
                item = fclr.get_Event(topic=topic, name=name, records=records)

            if not item:
                return f"Couldn't find {action} **{topic} {item}**."
            text = f"**{action} on topic {topic}:\n-> {name}** `{item}`"
            return text

        #  Topic
        if action == "note":
            topic = fclr.get_Notes_Topic(topic=topic, records=records)
        else:
            topic = fclr.get_Events_Topic(topic=topic, records=records)

        if not topic:
            return f"Couldn't find {action}s on topic **{topic}**."
        return topic

    #  Get messages
    #  Argument Validation
    if len(args) != 1 or type(args[0]) == list:
        return "I don't understand :/\nCorrect command to get remembered message:\n`sr! get [name]`"
    
    name = args[0]
    found = fclr.get_Message(name, records)
    if found:
        return f"Searching through memories for **{name}**..."

    return f"I don't remember the message **{name}**"


def forget(args, records):
    action = args[0].lower()
    if action in  ["note", "event"]:
        # Argument Validations
        if not len(args) in [3, 2]:
            return f"I don't understand :/\nCorrect command to forget {action}:\n`sr! forget {action} [topic] [name(optional)]`"

        topic = args[1].upper()
        if len(args) == 3:
            name = args[2].upper()
            if action == "note":
                deleted = fclr.delete_Note(topic=topic, name=name, records=records)
            else:
                deleted = fclr.delete_Event(topic=topic, name=name, records=records)

            if deleted:
                return f"{action} **{name}** deleted from topic **{topic}**."

            return f"Couldn't find {action} **{topic} {name}**."

        if action == "note":
            deleted = fclr.delete_Notes_Topic(topic=topic, records=records)
        else:
            deleted = fclr.delete_Events_Topic(topic=topic, records=records)

        if deleted:
                response = f"{action} topic **{topic}** deleted."
                return response
        response = f"Couldn't find {action} topic **{topic}**."
        return response

    #  Forget Messages
    #  Argument Validation
    if len(args) != 1:
        return "I don't understand :/\nCorrect command to forget:\n`sr! forget [name]`"
    
    name = args[0]
    deleted = fclr.delete_Message(name, records)
    if deleted:
        return f"**{name}** forgotten."

    return f"Couldn't find a message named **{name}**"


def add(args, records):
    action = args[0]
    action_caps = action.upper()
    if action_caps in ["NOTE", "EVENT"]:
        #  Argument Validations
        if not len(args) in [4, 3]:
            return f"I don't understand :/\nCorrect command to add {action}:\n`sr! {action} add [topic] [{action}_name] [item]`"

        topic = args[1].upper()
        #  Multiple entries
        if type(args[2]) == list:
            entries = args[2]
            names = []
            added = True
            for entry in entries:
                name = entry[0].upper()
                names.append(name)
                if action_caps == "NOTE":
                    names += name + ", "
                    item = entry[1]
                    #  Validations
                    if not len(item)<=ALLOWED_NOTE_CHARACTERS and len(item)>0:
                        return f"Note {name} should be less than 240 characters"
                    added = fclr.add_Note(records=records, topic=topic, name=name, item=item)
                else:
                    date = entry[1]
                    #  Validations
                    if not vclr.is_Correct_Date_Format(date):
                        return f"On event {name} date format should be Day/Month/Year"

                    if vclr.get_Days_Left(date) < 0:
                        return f"Event **{name}** date `{date}` has already passed.\nIf you still want me to remember it, add a note."
                    added = fclr.add_Event(records=records, topic=topic, name=name, date=date)

            if added:
                return f"{action} **{names}** added in topic **{topic}**."

            return f"One or more of {action}s **{names}** already exists in topic **{topic}**."

        #  Single entry
        name = args[2].upper()
        item = args[3].upper()

        if action_caps == "NOTE":
            #  Validations
            if not len(item)<=ALLOWED_NOTE_CHARACTERS and len(item)>0:
                return "Notes should be less than 240 characters"

            added = fclr.add_Note(records=records, topic=topic, name=name, item=item)
        else:
            #  Validations
            if not vclr.is_Correct_Date_Format(item):
                return "Date format should be Day/Month/Year"

            if vclr.get_Days_Left(item) < 0:
                return f"Event **{name}** date `{item}` has already passed.\nIf you still want me to remember it, add a note."
            
            added = fclr.add_Event(records=records, topic=topic, name=name, date=item)

        if added:
            return f"{action} **{name}** added in topic **{topic}**."
        return f"A {action} with the name **{name}** already exists in topic **{topic}**."


def edit(args, records):
    action = args[0]
    action_caps = action.upper()
    if action_caps in ["NOTE", "EVENT"]:
        #  Argument Validations
        if not len(args) in [4, 3]:
            return f"I don't understand :/\nCorrect command to edit {action}:\n`sr! edit {action} [topic] [{action}_name] [item]`"

        topic = args[1].upper()
        #  Multiple entries
        if type(args[2]) == list:
            entries = args[2]
            names = []
            edited = True
            for entry in entries:
                name = entry[0].upper()
                names.append(name)
                if action_caps == "NOTE":
                    names += name + ", "
                    item = entry[1]
                    #  Validations
                    if not len(item)<=ALLOWED_NOTE_CHARACTERS and len(item)>0:
                        return f"Note {name} should be less than 240 characters"
                    edited = fclr.edit_Note(records=records, topic=topic, name=name, item=item)
                else:
                    date = entry[1]
                    #  Validations
                    if not vclr.is_Correct_Date_Format(date):
                        return f"On event {name} date format should be Day/Month/Year"

                    if vclr.get_Days_Left(date) < 0:
                        return f"Event **{name}** date `{date}` has already passed.\nIf you still want me to remember it, edit a note."
                    edited = fclr.edit_Event(records=records, topic=topic, name=name, date=date)

            if edited:
                return f"{action} **{names}** edited in topic **{topic}**."

            return f"One or more of {action}s **{names}** don't exist in topic **{topic}**."

        #  Single entry
        name = args[2].upper()
        item = args[3].upper()

        if action_caps == "NOTE":
            #  Validations
            if not len(item)<=ALLOWED_NOTE_CHARACTERS and len(item)>0:
                return "Notes should be less than 240 characters"

            edited = fclr.edit_Note(records=records, topic=topic, name=name, item=item)
        else:
            #  Validations
            if not vclr.is_Correct_Date_Format(item):
                return "Date format should be Day/Month/Year"

            if vclr.get_Days_Left(item) < 0:
                return f"Event **{name}** date `{item}` has already passed.\nIf you still want me to remember it, add a note."
            
            edited = fclr.edit_Event(records=records, topic=topic, name=name, date=item)

        if edited:
            return f"{action} **{name}** edited in topic **{topic}**."
        return f"A {action} with the name **{name}** doesn't exist in topic **{topic}**."


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

    action =  args[0].upper()
    if action == "URGENT":
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

    else:
        return f"I don't know how to perform the action **{action}**."
