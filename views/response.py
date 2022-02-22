from controllers import FeatureController as fclr
from controllers import ValidationController as vclr
from controllers import PersistenceController as pclr
from settings import ALLOWED_NOTE_CHARACTERS

async def main(message, features, server):
    #  Getting server records
    records = await pclr.load_Records(server)
    
    commands = vclr.get_Commands(message.content)
    command = commands[0].upper()

    #  Special feature cases
    if command == "HELP":  #  Case: Requires all feature list
        descriptions = fclr.get_Commands_Description(features)
        response = "**Commands**\n"
        for description in descriptions:
            if description:
                response += description + "\n"
        response += "**-> Examples on:** `https://github.com/ihammadasghar/SrEngenheiro/blob/main/README.md`"
        await message.channel.send(response, embed=None)
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

    await message.channel.send(f"Sorry senhor, I don't understand.\n Is this french?")
    return


def greet(message):
    tag = message.author.display_name
    return f"Hi Sr.{tag}! `!help` to see how I can be of help."


def today():
    date_Today = fclr.get_Date_Today()
    return f"Date today is `{date_Today}.`"

#  Easter Egg
def praise():
    return "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧"

#  Easter Egg
def scold():
    return "ಥ_ಥ"


def messages(args, records):
    #  Topic tags
    if len(args) == 0:
        topic_names = fclr.get_Topic_Names(table="MESSAGES", records=records)
        if topic_names is None:
            return "There are no messages in my memory senhor."

        response = f"**Messages**\n"
        tag_names = fclr.get_Topic_Tag_Names(table="MESSAGES", topic="REMEMBERED", records=records)
        for tag in tag_names:
            response += f"-> {tag}\n"
        
        return response


def remember_Message(args, records, message):
    #  Argument Validations
    if len(args) != 1 or type(args[0]) == list:
        return "Senhor, I don't understand\nCorrect command to remember:\n`!remember [tag]`"
    
    if message.reference.message_id == None:
        return "Senhor, you need to reply this command to the message I need to remember."


    tag = args[0]
    added = fclr.add_Message(tag, message.reference.message_id, records)
    if added:
        return f"I'll keep an eye on **{tag}** senhor!"

    return f"Senhor, a message with the tag **{tag}** already exists"


def get(args, records):
    action =  args[0].lower()
    if action in ["note", "event"]:
        #  Argument Validations
        if not len(args) in [3, 2, 1]:
            response = f"Sorry senhor, I dont understand\n Correct command to get {action}:\n`!get {action} [topic] [tag(optional)]`"
            return response

        #  Single content
        topic = args[1].upper()
        if len(args) == 3:
            tag = args[2].upper()
            if action == "note":
                content = fclr.get_Note(topic=topic, tag=tag, records=records)
            else:
                content = fclr.get_Event(topic=topic, tag=tag, records=records)

            if not content:
                return f"Sorry senhor, I couldn't find {action} **{topic} {tag}**."

            text = f"**{action} on topic {topic}:\n-> {tag}** `{content}`"
            return text

        #  Topic
        if action == "note":
            content = fclr.get_Notes_Topic(topic=topic, records=records)
            if not content:
                content = fclr.get_Note(topic="GENERAL", tag=topic, records=records)
                if not content:
                    return f"Sorry senhor, I couldn't find {action} **{topic}** in GENERAL notes."
                return f"**{action} on topic GENERAL:\n-> {topic}** `{content}`"
            return content
        else:
            content = fclr.get_Events_Topic(topic=topic, records=records)
            if not content:
                content = fclr.get_Event(topic="GENERAL", tag=topic, records=records)
                if not content:
                    return f"Sorry senhor, I couldn't find {action} **{topic}** in GENERAL events."
                return f"**{action} on topic GENERAL:\n-> {topic}** `{content}`"
            return content

    #  Get messages
    #  Argument Validation
    if len(args) != 1 or type(args[0]) == list:
        return "Sorry senhor,  I don't understand\nCorrect command to get remembered message:\n`!get [tag]`"
    
    tag = args[0]
    found = fclr.get_Message(tag, records)
    if found:
        return f"Searching through memories for **{tag}**..."
    return f"Sorry senhor, I don't remember the message **{tag}**"


def forget(args, records):
    action = args[0].lower()
    if action in  ["note", "event"]:
        # Argument Validations
        if not len(args) in [3, 2]:
            return f"Sorry senhor, I dont understand\nCorrect command to forget {action}:\n`!forget {action} [topic] [tag(optional)]`"

        topic = args[1].upper()
        if len(args) == 3:
            tag = args[2].upper()
            if action == "note":
                deleted = fclr.delete_Note(topic=topic, tag=tag, records=records)
            else:
                deleted = fclr.delete_Event(topic=topic, tag=tag, records=records)

            if deleted:
                return f"{action} **{tag}** forgotten from topic **{topic}**."

            return f"Sorry senhor, I couldn't find {action} **{topic} {tag}**."

        if action == "note":
            deleted = fclr.delete_Notes_Topic(topic=topic, records=records)
        else:
            deleted = fclr.delete_Events_Topic(topic=topic, records=records)

        if deleted:
                response = f"{action} topic **{topic}** forgotten, senhor!"
                return response
        response = f"Sorry senhor, I couldn't find {action} topic **{topic}**, sorry senhor\nTo forget note/event:`!forget {action} [topic] [tag(optional)]`"
        return response

    #  Forget Messages
    #  Argument Validation
    if len(args) != 1:
        return "Sorry senhor, I dont understand\nCorrect command to forget:\n`!forget [tag]`"
    
    tag = args[0]
    deleted = fclr.delete_Message(tag, records)
    if deleted:
        return f"**{tag}** forgotten."

    return f"Sorry senhor, I couldn't find a message tag **{tag}**."


def add(args, records):
    action = args[0].lower()
    if action in ["note", "event"]:
        #  Argument Validations
        if not len(args) in [4, 3, 2]:
            return f"Sorry senhor, I dont understand\nCorrect command to add {action}:\n`!{action} add [topic] [{action}_tag] [content]`"

        #  Multiple entries
        mult_entries = False
        if len(args)==3 and type(args[2]) == list:
            topic = args[1]
            entries = args[2]
            mult_entries = True

        elif type(args[1]) == list:
            topic = "GENERAL"
            entries = args[1]
            mult_entries = True

        if mult_entries:
            tags = []
            for entry in entries:
                tag = entry[0].upper()
                tags.append(tag)
                if action == "note":
                    content = entry[1]
                    #  Validations
                    if not len(content) <= ALLOWED_NOTE_CHARACTERS and len(content)>0:
                        return f"Senhor! note {tag} should be less than 240 characters"
                    added = fclr.add_Note(records=records, topic=topic, tag=tag, content=content)
                else:
                    date = entry[1]
                    #  Validations
                    if not vclr.is_Correct_Date_Format(date):
                        return f"Senhor! on event {tag} date format should be Day/Month/Year"

                    if vclr.get_Days_Left(date) < 0:
                        return f"Senhor! event **{tag}** date `{date}` has already passed.\nIf you still want me to remember it, add a note."
                    added = fclr.add_Event(records=records, topic=topic, tag=tag, date=date)
                if not added:
                    return f"Senhor! {action} **{tag}** already exists in topic **{topic}**."
            return f"{action}s **{tags}** added in topic **{topic}** senhor!"

        #  Single entry
        if len(args) == 4:
            topic = args[1].upper()
            tag = args[2].upper()
            content = args[3]
        else:
            topic = "GENERAL"
            tag = args[1].upper()
            content = args[2]

        if action == "note":
            #  Validations
            if not len(content)<=ALLOWED_NOTE_CHARACTERS and len(content)>0:
                return "Senhor! notes should be less than 240 characters"

            added = fclr.add_Note(records=records, topic=topic, tag=tag, content=content)
        else:
            #  Validations
            if not vclr.is_Correct_Date_Format(content):
                return "Senhor! date format should be Day/Month/Year"

            if vclr.get_Days_Left(content) < 0:
                return f"Senhor! event **{tag}** date `{content}` has already passed.\nIf you still want me to remember it, add a note."
            
            added = fclr.add_Event(records=records, topic=topic, tag=tag, date=content)

        if added:
            return f"{action} **{tag}** added in topic **{topic}** senhor."
        return f"Senhor! a {action} with the tag **{tag}** already exists in topic **{topic}**."
    return f"Sorry senhor, I don't know what {action} is."


def edit(args, records):
    action = args[0].lower()
    if action in ["note", "event"]:
        #  Argument Validations
        if not len(args) in [4, 3, 2]:
            return f"Sorry senhor, I dont understand\nCorrect command to edit {action}:\n`!edit {action} [topic] [{action}_tag] [content]`"

        #  Multiple entries
        mult_entries = False
        
        if len(args)==3 and type(args[2]) == list:
            topic = args[1]
            entries = args[2]
            mult_entries = True
        elif type(args[1]) == list:
            topic = "GENERAL"
            entries = args[1]
            mult_entries = True

        if mult_entries:
            tags = []
            for entry in entries:
                tag = entry[0].upper()
                tags.append(tag)
                if action == "note":
                    tags += tag + ", "
                    content = entry[1]
                    #  Validations
                    if not len(content)<=ALLOWED_NOTE_CHARACTERS and len(content)>0:
                        return f"Senhor! note {tag} should be less than 240 characters"
                    edited = fclr.edit_Note(records=records, topic=topic, tag=tag, content=content)
                else:
                    date = entry[1]
                    #  Validations
                    if not vclr.is_Correct_Date_Format(date):
                        return f"Senhor! on event {tag} date format should be Day/Month/Year"

                    if vclr.get_Days_Left(date) < 0:
                        return f"Senhor! event **{tag}** date `{date}` has already passed.\nIf you still want me to remember it, edit a note."
                    edited = fclr.edit_Event(records=records, topic=topic, tag=tag, date=date)
                if not edited:
                    return f"Senhor! {action} **{tag}** doesn't exist in topic **{topic}**."

                return f"{action} **{tags}** edited in topic **{topic}** senhor!"

        #  Single entry
        if len(args) == 4:
            topic = args[1].upper()
            tag = args[2].upper()
            content = args[3]
        else:
            topic = "GENERAL"
            tag = args[1].upper()
            content = args[2]

        if action == "note":
            #  Validations
            if not len(content) <= ALLOWED_NOTE_CHARACTERS and len(content)>0:
                return "Senhor! notes should be less than 240 characters"

            edited = fclr.edit_Note(records=records, topic=topic, tag=tag, content=content)
        else:
            #  Validations
            if not vclr.is_Correct_Date_Format(content):
                return "Senhor! Date format should be Day/Month/Year"

            if vclr.get_Days_Left(content) < 0:
                return f"Senhor! event **{tag}** date `{content}` has already passed.\nIf you still want me to remember it, add a note."
            
            edited = fclr.edit_Event(records=records, topic=topic, tag=tag, date=content)

        if edited:
            return f"{action} **{tag}** edited in topic **{topic}** senhor!."
        return f"Senhor! {action} with the tag **{tag}** doesn't exist in topic **{topic}**."
    return f"Sorry senhor, I don't know what {action} is."


def notes(records):
    #  Topic tags
    topic_names = fclr.get_Topic_Names(table="NOTES", records=records)
    if topic_names is None:
        return "There are no added notes senhor."

    response = f"**Notes**\n"
    for name in topic_names:
        response += f"**-> {name}:**\n"
        tag_names = fclr.get_Topic_Tag_Names("NOTES", name, records)
        for tag in tag_names:
            response += f" - {tag}\n"
    
    return response


def events(args, records):
    # Listing Ordered Events
    #  Argument Validations
    if len(args) == 0:
        all_events = fclr.get_Ordered_Events(records)
        if all_events is None:
            return "There are no upcoming added events senhor."

        response = "**Upcoming events:**\n"
        for event in all_events:
            response += f"-> `{event['Date']}` - **({event['Topic']})** {event['Tag']}\n"
        return response

    action =  args[0].upper()
    if action == "URGENT":
        response = fclr.urgent_Events(records)
        if response == "**Urgent events:**\n":
            response = "Nothing urgent, no events in the next 7 days senhor."
        return response

    elif action == "TOPICS":
        topic_names = fclr.get_Topic_Names(table="EVENTS", records=records)
        if topic_names is None:
            return "There are no added events senhor."

        response = f"**Events**\n"
        for name in topic_names:
            response += f"**-> {name}:**\n"
            tag_names = fclr.get_Topic_Tag_Names("EVENTS", name, records)
            for tag in tag_names:
                response += f" - {tag}\n"
        
        return response

    return f"Sorry senhor, I don't know what {action} is."
