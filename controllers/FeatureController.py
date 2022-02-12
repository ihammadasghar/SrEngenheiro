# from feature_registry import features
import datetime
from datetime import date



# async def greet(self):
#     await self.message.channel.send(f"Hi {self.message.author.nick}! Sr.Engenheiro here\n-> sr! help: To see how I can help")
#     return


# async def today(self):
#     date_Today = date.today()
#     date_Today = today.strftime("%d/%m/%Y")
#     await self.message.channel.send(f"Today's date is {date_Today}")
#     return


# async def praise(self):
#     await self.message.channel.send(f"(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧")
#     return


# async def event(self, action, topic, name=None, date=None):
#     action = action.upper()
#     topic = topic.upper()

#     if action == "ADD":
#         if name is None:
#             await self.message.channel.send(f"Missing event name.")
#             return
#         name = name.upper()
#         record = [{"name": name, "item": date}]
#         await self.records.add(topic=topic, records=record)
#         await self.message.channel.send(f"{name} added to {topic}.")
#         return
    
#     elif action == "GET":
#         records = self.records.get(topic=topic)
#         records.sort(key=lambda x: datetime.datetime.strptime(x['item'], '%d/%m/%Y'))

#         #  In case topic doesnt exist
#         if records is None:
#             await self.message.channel.send(f"Sorry, I have no records of the topic {topic}")
#             return

#         if not name is None:
#             name = name.upper()

#             for record in records:
#                 if record["name"] == name:
#                     await self.message.channel.send(f"{topic}: {name} - {record}.")
#                     return
#             #  Record not found
#             await self.message.channel.send(f"Sorry, I have no record of {name} in the topic {topic}.")
#             return

#         result = topic
#         for record in records:
#             result += "\n-> " + record["name"] + " " + record["item"]

#         await self.message.channel.send(result)
#         return


#     elif action == "DELETE":
#         if name is None:
#             await self.message.channel.send(f"Missing event name.")
#             return
#         name = name.upper()
#         is_Removed = await self.records.remove(topic, record_Name=name)
#         if not is_Removed:
#             await self.message.channel.send(f"No such record exists.")
#             return
#         await self.message.channel.send(f"{name} removed from {topic}.")
#         return
    
#     else:
#         await self.message.channel.send(f"I don't know how to perform action {action} :(")
#         return


# def sort_dates(self,events):
#     sorted_events = {}
#     events_list = []
#     for event in events.items():
#         events_list.append({"name": event[0], "date": event[1]})
#     events_list.sort(key=lambda x: datetime.datetime.strptime(x['date'], '%d/%m/%Y'))

#     for event in events_list:
#         sorted_events.update({event["name"]:event["date"]})

#     return sorted_events


# async def event(self, action, topic, name=None, date=None):
#     action = action.upper()
#     topic = topic.upper()

#     if action == "ADD":
#         name = name.upper()
#         record = {name: date}
#         await self.records.add(topic=topic, records=record)
#         await self.message.channel.send(f" I'll add {name} to {topic}.")
#         return

#     elif action == "GET":
#         records = self.records.get(topic=topic)
#         records = self.sort_dates(records)

#         #  In case topic doesnt exist
#         if records is None:
#             await self.message.channel.send(f"Sorry, I have no records of the event {topic}")
#             return

#         if not name is None:
#             name = name.upper()

#             #  In case the name doesnt exist in the topic
#             try:
#                 record = records[name]
#             except KeyError:
#                 await self.message.channel.send(f"Sorry, I have no record of {name} in the event {topic}.")
#                 return

#             await self.message.channel.send(f"{topic}: {name} - {record}.")
#             return

#         result = topic
#         for record in records.items():
#             result += "\n" + record[0] + " " + record[1]

#         await self.message.channel.send(result)
#         return

#     elif action == "DELETE":
#         name = name.upper()
#         is_removed = await self.records.remove(topic, record_Key=name)
#         if not is_removed:
#             await self.message.channel.send(f"No such record exists.")
#             return
#         await self.message.channel.send(f" I'll remove {name} from {topic}.")
#         return

#     else:
#         await self.message.channel.send(f"I don't know how to perform action {action} :(")
#         return


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

