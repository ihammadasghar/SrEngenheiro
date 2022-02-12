# from feature_registry import features
import datetime
from datetime import date



async def greet(self):
    await self.message.channel.send(f"Hi {self.message.author.nick}! Sr.Engenheiro here\n-> sr! help: To see how I can help")
    return


async def today(self):
    date_Today = date.today()
    date_Today = today.strftime("%d/%m/%Y")
    await self.message.channel.send(f"Today's date is {date_Today}")
    return


def get_Commands_Description(features):
    text = "COMMANDS"
    for feature in features:
        text += "\n-> " + feature.description
    
    return text


async def add_Note(topic, name, item, records):
    note = {name: item}
    await records.update(table="NOTES", topic=topic, records=note)
    return


async def get_Note(records, topic, name):
    note = await records.get(table="NOTES", topic=topic)
    if not note:
        return None
    text = f"Note on topic {topic}:\n-> {name} - {note[name]}"
    return text


async def get_Notes_Topic(records, topic):
    notes = await records.get(table="NOTES", topic=topic)
    if not notes:
        return None

    text = f"Note on topic {topic}:\n"
    for name in notes.keys():
        text += f"-> {name} - {notes[name]}\n" 
    return text


def delete_Note(records, topic, name):
    deleted = records.remove(table="NOTES", topic=topic, name=name)
    return deleted


def delete_Notes_Topic(records, topic):
    deleted = records.remove(table="NOTES", topic=topic)
    return deleted


async def add_Event(topic, name, date, records):
    event = {name: date}
    await records.update(table="EVENTS", topic=topic, records=event)
    return


async def get_Event(records, topic, name):
    event = await records.get(table="EVENTS", topic=topic)
    if not event:
        return None
    text = f"Event on topic {topic}:\n-> {name} - {event[name]}"
    return text


async def get_Events_Topic(records, topic):
    events = await records.get(table="EVENTS", topic=topic)
    if not events:
        return None

    #  Sorting events acording to dates
    events = dict(sorted(events.items(), key=lambda x: datetime.datetime.strptime(x[1], '%d/%m/%Y')))

    text = f"Event on topic {topic}:\n"
    for name in events.keys():
        text += f"-> {name} - {events[name]}\n" 
    return text


def delete_Event(records, topic, name):
    deleted = records.remove(table="EVENTS", topic=topic, name=name)
    return deleted


def delete_Events_Topic(records, topic):
    deleted = records.remove(table="EVENTS", topic=topic)
    return deleted