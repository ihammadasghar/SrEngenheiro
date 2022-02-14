import datetime
from datetime import date
from pydoc_data.topics import topics


def get_Date_Today():
    date_Today = date.today()
    date_Today = date_Today.strftime("%d/%m/%Y")
    return date_Today


def get_Commands_Description(features):
    text = "**COMMANDS**\n"
    for feature in features:
        text += feature.description + "\n"
    
    return text


def add_Note(topic, name, item, records):
    note = {name: item}
    records.update(table="NOTES", topic=topic, records=note)
    return


def get_Note(records, topic, name):
    note = records.get(table="NOTES", topic=topic)
    if not note:
        return None
    text = f"**Note on topic {topic}:\n-> {name}** ```{note[name]}```"
    return text



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


def add_Event(topic, name, date, records):
    event = {name: date}
    records.update(table="EVENTS", topic=topic, records=event)
    return


def get_Event(records, topic, name):
    event = records.get(table="EVENTS", topic=topic)
    if not event:
        return None
    text = f"**Event on topic {topic}:\n-> {name}** `{event[name]}`"
    return text



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


def add_Event(topic, name, date, records):
    event = {name: date}
    records.update(table="EVENTS", topic=topic, records=event)
    return


def get_Event(records, topic, name):
    event = records.get(table="EVENTS", topic=topic)
    if not event:
        return None
    text = f"**Event on topic {topic}:\n-> {name}** `{event[name]}`"
    return text



def get_Events_Topic(records, topic):
    events = records.get(table="EVENTS", topic=topic)
    if not events:
        return None

    #  Sorting events acording to dates
    events = dict(sorted(events.items(), key=lambda x: datetime.datetime.strptime(x[1], '%d/%m/%Y')))

    text = f"**Events on topic {topic}:**\n"
    for name in events.keys():
        text += f"**-> {name}** `{events[name]}`\n" 
    return text


def num_days(date_1,date_2):
    return (date_2-date_1).days

def urgent_Events(records):
    today = date.today()
    date_today = today.strftime("%Y/%m/%d")
    d_today = date_today.split("/")
    date_today = date(int(d_today[0]), int(d_today[1]), int(d_today[2]))
    table = records.get(table="EVENTS")
    topics_list = []
    for topic in table.items():
        topics_list.append(topic)
    events_list = []
    for topic in topics_list:
        for event in topic[1].items():
            events_list.append(event)
    if not events_list:
        return None

    #  Sorting events acording to dates
    events_list = dict(sorted(events_list, key=lambda x: datetime.datetime.strptime(x[1], '%d/%m/%Y')))

    text = f"**Urgent events:**\n"
    for event in events_list.keys():
        date_list = events_list[event].split("/")
        date_event = date(int(date_list[2]),int(date_list[1]),int(date_list[0]))
        days_left = num_days(date_event,date_today)*-1
        if  7>= days_left >= 0:
            if days_left < 1:
                text += f"**-> {event}** `Is due today!`\n" 
            else:
                if days_left == 1:
                    text += f"**-> {event}** `Due in:` **{days_left} day**\n" 
                else:
                    text += f"**-> {event}** `Due in:` **{days_left} days**\n" 
    return text



def delete_Event(records, topic, name):
    deleted = records.remove(table="EVENTS", topic=topic, name=name)
    return deleted


def delete_Events_Topic(records, topic):
    deleted = records.remove(table="EVENTS", topic=topic)
    return deleted


def get_Commands(command):
    parts = command.split("\n")
    commands =  parts[0].split('"')
    if len(commands) == 3:
        quotes_text = commands[1]
        commands = commands[0].split(" ")
        commands.pop()
        commands.append(quotes_text)
    else:
        commands = commands[0].split(" ")

    if len(commands) < 2:
        return ["sr!", "hi"]
    
    if len(parts) > 1:
        items = []
        for item in parts[1:]:
            item = item.split('"')
            if len(item) == 3:
                quotes_text = item[1]
                item = item[0].split(" ")
                item.pop()
                item.append(quotes_text)
            else:
                item = item[0].split(" ")
            items.append(item)
        commands.append(items)

    return commands


def get_Args(commands, feature, records, message):
    #  Arguments validations
    if type(feature.nargs) == list:
        if len(commands)-2 in feature.nargs:
            arguments = [commands[i+2] for i in range(len(commands)-2)]
        else:
            return None

    elif len(commands)-2 == feature.nargs: 
        arguments = [commands[i+2] for i in range(len(commands)-2)]
    else:
        return None

    params = []
    if not feature.nargs == 0:
        params.append(arguments)

    if feature.records_Required:
        params.append(records)

    if feature.message_Required:
        params.append(message)
    return params