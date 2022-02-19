from datetime import datetime, date
from .ValidationController import get_Days_Left


def get_Date_Today():
    date_Today = date.today()
    date_Today = date_Today.strftime("%d/%m/%Y")
    return date_Today


def get_Commands_Description(features):
    text = "**COMMANDS**\n"
    for feature in features:
        text += feature.description + "\n"
    
    return text

#  Remembered messages
def add_Message(name,  message_ID, records):
    added = records.create(table="MESSAGES", topic="REMEMBERED", name=name, item=message_ID)
    return added


def get_Message(name, records):
    message_ID = records.get(table="MESSAGES", topic="REMEMBERED", name=name)
    if message_ID:
        records.requested_message_ID = message_ID
        return True

    return False


def delete_Message(name, records):
    removed = records.remove(table="MESSAGES", topic="REMEMBERED", name=name)
    return removed

#  Notes
def edit_Note(topic, name, item, records):
    edited = records.update(table="NOTES", topic=topic, name=name, item=item)
    return edited


def add_Note(topic, name, item, records):
    created = records.create(table="NOTES", topic=topic, name=name, item=item)
    return created


def get_Note(records, topic, name):
    note = records.get(table="NOTES", topic=topic)
    if not note:
        return None
    text = f"**Note on topic {topic}:\n-> {name}** ```{note[name]}```"
    return text


def get_Notes(records):
    notes_table = records.get(table="NOTES")
    note_topic_names = notes_table.keys()
    if note_topic_names:
        return note_topic_names
    return None


def get_Notes_Topic(records, topic):
    notes = records.get(table="NOTES", topic=topic)
    if not notes:
        return None

    text = f"**Notes on topic {topic}:**\n"
    for name in notes.keys():
        text += f"**-> {name}** ```{notes[name]}```\n" 
    return text


def delete_Note(records, topic, name):
    deleted = records.remove(table="NOTES", topic=topic, name=name)
    return deleted


def delete_Notes_Topic(records, topic):
    deleted = records.remove(table="NOTES", topic=topic)
    return deleted

#  Events
def get_Ordered_Events(records):
    delete_Expired_Events(records)

    events = records.get(table="EVENTS")

    if events is None:
        return None

    #  Events across all topics
    all_events = []
    for topic in events.keys():
        topic_events = [{"Topic": topic,"Name": name, "Date": events[topic][name]} for name in events[topic].keys()]
        all_events += topic_events

    all_events.sort(key=lambda x: datetime.strptime(x["Date"], '%d/%m/%Y'))
    return all_events


def delete_Expired_Events(records):
    events = records.get(table="EVENTS")
    expired_events = []
    for topic in events.keys():
        for name in events[topic].keys():
            days_Left = get_Days_Left(events[topic][name])
            if days_Left<0:
                expired_events.append((topic, name))
    
    #  Removing expired events
    for event in expired_events:
        records.remove(table="EVENTS", topic=event[0], name=event[1])


def edit_Event(topic, name, date, records):
    edited = records.update(table="EVENTS", topic=topic, name=name, item=date)
    return edited


def add_Event(topic, name, date, records):
    created = records.create(table="EVENTS", topic=topic, name=name, item=date)
    return created


def get_Event(records, topic, name):
    delete_Expired_Events(records)
    event = records.get(table="EVENTS", topic=topic, name=name)
    return event


def get_Events(records):
    events_table = records.get(table="EVENTS")
    event_topic_names = events_table.keys()
    if event_topic_names:
        return event_topic_names
    return None


def get_Events_Topic(records, topic):
    events = records.get(table="EVENTS", topic=topic)
    if not events:
        return None

    #  Sorting events acording to dates
    events = dict(sorted(events.items(), key=lambda x: datetime.strptime(x[1], '%d/%m/%Y')))

    text = f"**Events on topic {topic}:**\n"
    for name in events.keys():
        text += f"**-> {name}** `{events[name]}`\n" 
    return text


def urgent_Events(records):
    delete_Expired_Events(records)
    table = records.get(table="EVENTS")
    events = []
    for topic in table.keys():
        for event in table[topic].items():
            events.append(event)

    if events == []:
        return None

    #  Sorting and events acording to dates
    events.sort(key=lambda x: datetime.strptime(x[1], '%d/%m/%Y'))
    
    text = f"**Urgent events:**\n"
    for event in events:
        days_Left = get_Days_Left(event[1])
        if  7>= days_Left:
            if days_Left == 1:
                text += f"**-> {event[0]}** `Is due today!`\n" 
            elif days_Left == 1:
                text += f"**-> {event[0]}** `Due in:` **{days_Left} day**\n" 
            else:
                text += f"**-> {event[0]}** `Due in:` **{days_Left} days**\n"
    return text


def delete_Event(records, topic, name):
    deleted = records.remove(table="EVENTS", topic=topic, name=name)
    return deleted


def delete_Events_Topic(records, topic):
    deleted = records.remove(table="EVENTS", topic=topic)
    return deleted
