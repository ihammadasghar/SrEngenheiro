from models.Feature import Feature
import datetime
from datetime import date


class FeatureController:
    def __init__(self, message, server) -> None:
        self.features = self.get_Features()
        self.server = server
        self.records = server.records
        self.message = message

    def get_Features(self):
        #  Intialize your feature here
        greeting_feature =  Feature(command="HI", 
                                    args=0, 
                                    functionality=self.greet, 
                                    description="Hi: greetings!"
                                    )
        
        current_day_feature = Feature(command="TODAY",
                                    args=0,
                                    functionality=self.today,
                                    description="TODAY: Tells the current date."
                                    )               

        praise_feature = Feature(command="GOOD-BOT",
                                    args=0, 
                                    functionality=self.praise,
                                    description="PRAISE: ???."
                                    )
            
        get_help_feature = Feature(command="HELP", 
                                    args=0, 
                                    functionality=self.get_help,
                                    description="HELP: Lists all commands."
                                    )

        event_feature = Feature(command="EVENTS", 
                                    args=[2, 3, 4], 
                                    functionality=self.event, 
                                    description="EVENTS [action] [topic] [name] [date]: Adds events (e.g. event add Testes AP 22/4/2022)\n Possible Actions:\n  - Add\n  - Delete\n  - Get"
                                    )
        
        note_feature = Feature(command="NOTES", 
                                args=[2, 3, 4], 
                                functionality=self.note, 
                                description="NOTES [action] [topic] [name] [item]: Makes notes (e.g. notes add Links youtube https://youtube.com)\n  Possible Actions:\n  - Add\n  - Delete\n  - Get"
                                )

        #  Add the initialized feature here

        features = [greeting_feature, current_day_feature, praise_feature, get_help_feature, event_feature, note_feature]

        return features


    async def greet(self):
        await self.message.channel.send(f"Hi {self.message.author.nick}! Sr.Engenheiro here\n-> sr! help: To see how I can help")
        return

    
    async def today(self):
        date_Today = date.today()
        date_Today = today.strftime("%d/%m/%Y")
        await self.message.channel.send(f"Today's date is {date_Today}")
        return

    
    async def praise(self):
        await self.message.channel.send(f"(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧")
        return
 

    async def event(self, action, topic, name=None, date=None):
        action = action.upper()
        topic = topic.upper()

        if action == "ADD":
            if name is None:
                await self.message.channel.send(f"Missing event name.")
                return
            name = name.upper()
            record = [{"name": name, "item": date}]
            await self.records.add(topic=topic, records=record)
            await self.message.channel.send(f"{name} added to {topic}.")
            return
        
        elif action == "GET":
            records = self.records.get(topic=topic)
            records.sort(key=lambda x: datetime.datetime.strptime(x['item'], '%d/%m/%Y'))

            #  In case topic doesnt exist
            if records is None:
                await self.message.channel.send(f"Sorry, I have no records of the topic {topic}")
                return

            if not name is None:
                name = name.upper()

                for record in records:
                    if record["name"] == name:
                        await self.message.channel.send(f"{topic}: {name} - {record}.")
                        return
                #  Record not found
                await self.message.channel.send(f"Sorry, I have no record of {name} in the topic {topic}.")
                return

            result = topic
            for record in records:
                result += "\n-> " + record["name"] + " " + record["item"]

            await self.message.channel.send(result)
            return


        elif action == "DELETE":
            if name is None:
                await self.message.channel.send(f"Missing event name.")
                return
            name = name.upper()
            is_Removed = await self.records.remove(topic, record_Name=name)
            if not is_Removed:
                await self.message.channel.send(f"No such record exists.")
                return
            await self.message.channel.send(f"{name} removed from {topic}.")
            return
        
        else:
            await self.message.channel.send(f"I don't know how to perform action {action} :(")
            return


    def sort_dates(self,events):
        sorted_events = {}
        events_list = []
        for event in events.items():
            events_list.append({"name": event[0], "date": event[1]})
        events_list.sort(key=lambda x: datetime.datetime.strptime(x['date'], '%d/%m/%Y'))

        for event in events_list:
            sorted_events.update({event["name"]:event["date"]})

        return sorted_events


    async def event(self, action, topic, name=None, date=None):
        action = action.upper()
        topic = topic.upper()

        if action == "ADD":
            name = name.upper()
            record = {name: date}
            await self.records.add(topic=topic, records=record)
            await self.message.channel.send(f" I'll add {name} to {topic}.")
            return

        elif action == "GET":
            records = self.records.get(topic=topic)
            records = self.sort_dates(records)

            #  In case topic doesnt exist
            if records is None:
                await self.message.channel.send(f"Sorry, I have no records of the event {topic}")
                return

            if not name is None:
                name = name.upper()

                #  In case the name doesnt exist in the topic
                try:
                    record = records[name]
                except KeyError:
                    await self.message.channel.send(f"Sorry, I have no record of {name} in the event {topic}.")
                    return

                await self.message.channel.send(f"{topic}: {name} - {record}.")
                return

            result = topic
            for record in records.items():
                result += "\n" + record[0] + " " + record[1]

            await self.message.channel.send(result)
            return

        elif action == "DELETE":
            name = name.upper()
            is_removed = await self.records.remove(topic, record_Key=name)
            if not is_removed:
                await self.message.channel.send(f"No such record exists.")
                return
            await self.message.channel.send(f" I'll remove {name} from {topic}.")
            return
        
        else:
            await self.message.channel.send(f"I don't know how to perform action {action} :(")
            return


    async def get_help(self):
        text = "COMMANDS"
        features = self.get_Features()
        for feature in features:
            text += "\n-> " + feature.description
        
        await self.message.channel.send(text)
        return


    async def note(self, action, topic, name=None, item=None):
        action = action.upper()
        topic = topic.upper()
        

        if action == "ADD":
            if name is None:
                await self.message.channel.send(f"Missing name argument.")
                return
            name = name.upper()
            record = [{"name": name, "item": item}]
            await self.records.add(topic=topic, records=record)
            await self.message.channel.send(f"{name} added to {topic}.")
            return
        
        elif action == "GET":
            records = self.records.get(topic=topic)
            #  In case topic doesnt exist
            if records is None:
                await self.message.channel.send(f"Sorry, I have no records of the topic {topic}")
                return

            if not name is None:
                name = name.upper()

                for record in records:
                    if record["name"] == name:
                        await self.message.channel.send(topic + "\n-> " + record["name"] + " " + record["item"])
                        return
                #  Record not found
                await self.message.channel.send(f"Sorry, I have no record of {name} in the topic {topic}.")
                return

            result = topic
            for record in records:
                result += "\n-> " + record["name"] + " " + record["item"]

            await self.message.channel.send(result)
            return


        elif action == "DELETE":
            if name is None:
                await self.message.channel.send(f"Missing event name.")
                return
            name = name.upper()
            is_Removed = await self.records.remove(topic, record_Name=name)
            if not is_Removed:
                await self.message.channel.send(f"No such record exists.")
                return
            await self.message.channel.send(f"{name} deleted from {topic}.")
            return
        
        else:
            await self.message.channel.send(f"I don't know how to perform action {action} :(")
            return
