from datetime import datetime, date
from .ValidationController import get_Days_Left


def get_Date_Today():
    date_Today = date.today()
    date_Today = date_Today.strftime("%d/%m/%Y")
    return date_Today


def get_Commands_Description(features):
    description = [feature.description for feature in features]
    return description

#  Remembered messages
def add_Message(tag,  message_ID, records):
    added = records.create(table="MESSAGES", topic="REMEMBERED", tag=tag, content=message_ID)
    return added


def get_Message(tag, records):
    message_ID = records.get(table="MESSAGES", topic="REMEMBERED", tag=tag)
    if message_ID:
        records.requested_message_ID = message_ID
        return True

    return False


def delete_Message(tag, records):
    removed = records.remove(table="MESSAGES", topic="REMEMBERED", tag=tag)
    return removed

#  Notes
def edit_Note(topic, tag, content, records):
    edited = records.update(table="NOTES", topic=topic, tag=tag, content=content)
    return edited


def add_Note(topic, tag, content, records):
    created = records.create(table="NOTES", topic=topic, tag=tag, content=content)
    return created


def get_Note(records, topic, tag):
    note = records.get(table="NOTES", topic=topic, tag=tag)
    return note


def get_Notes(records):
    notes_table = records.get(table="NOTES")
    note_topic_tags = notes_table.keys()
    if note_topic_tags:
        return note_topic_tags
    return None


def get_Notes_Topic(records, topic):
    notes = records.get(table="NOTES", topic=topic)
    if not notes:
        return None

    text = f"**Notes on topic {topic}:**\n"
    for tag in notes.keys():
        text += f"**-> {tag}** ```{notes[tag]}```\n" 
    return text


def delete_Note(records, topic, tag):
    deleted = records.remove(table="NOTES", topic=topic, tag=tag)
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
        topic_events = [{"Topic": topic,"Tag": tag, "Date": events[topic][tag]} for tag in events[topic].keys()]
        all_events += topic_events

    all_events.sort(key=lambda x: datetime.strptime(x["Date"], '%d/%m/%Y'))
    return all_events


def delete_Expired_Events(records):
    events = records.get(table="EVENTS")
    expired_events = []
    for topic in events.keys():
        for tag in events[topic].keys():
            days_Left = get_Days_Left(events[topic][tag])
            if days_Left<0:
                expired_events.append((topic, tag))
    
    #  Removing expired events
    for event in expired_events:
        records.remove(table="EVENTS", topic=event[0], tag=event[1])


def edit_Event(topic, tag, date, records):
    edited = records.update(table="EVENTS", topic=topic, tag=tag, content=date)
    return edited


def add_Event(topic, tag, date, records):
    created = records.create(table="EVENTS", topic=topic, tag=tag, content=date)
    return created


def get_Event(records, topic, tag):
    delete_Expired_Events(records)
    event = records.get(table="EVENTS", topic=topic, tag=tag)
    return event


def get_Events(records):
    events_table = records.get(table="EVENTS")
    event_topic_tags = events_table.keys()
    if event_topic_tags:
        return event_topic_tags
    return None


def get_Events_Topic(records, topic):
    events = records.get(table="EVENTS", topic=topic)
    if not events:
        return None

    #  Sorting events acording to dates
    events = dict(sorted(events.contents(), key=lambda x: datetime.strptime(x[1], '%d/%m/%Y')))

    text = f"**Events on topic {topic}:**\n"
    for tag in events.keys():
        text += f"**-> {tag}** `{events[tag]}`\n" 
    return text


def urgent_Events(records):
    delete_Expired_Events(records)
    table = records.get(table="EVENTS")
    events = []
    for topic in table.keys():
        for event in table[topic].contents():
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


def delete_Event(records, topic, tag):
    deleted = records.remove(table="EVENTS", topic=topic, tag=tag)
    return deleted


def delete_Events_Topic(records, topic):
    deleted = records.remove(table="EVENTS", topic=topic)
    return deleted
