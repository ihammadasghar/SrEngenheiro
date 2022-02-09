from models.Feature import Feature

class FeatureController:
    def __init__(self, message, server) -> None:
        self.features = self.get_Features()
        self.server = server
        self.records = server.records
        self.message = message

    def get_Features(self):
        #  Intialize your feature here
        greeting_feature =  Feature(command="greet", 
                                    args=0, 
                                    functionality=self.greet, 
                                    description="greet: Be nice and say Hi to Sr.Engenheiro. :)"
                                    )

        get_help_feature =  Feature(command="help", 
                                    args=0, 
                                    functionality=self.get_help,
                                    description="help: Lists all commands."
                                    )

        add_event_feature = Feature(command="addevent", 
                                    args=2, 
                                    functionality=self.add_event, 
                                    description="addevent eventname date: Adds an event to the calendar."
                                    )
        
        note_feature = Feature(command="note", 
                                args=[2, 3, 4], 
                                functionality=self.note, 
                                description="note action topic name item: Saves a link as note (e.g. note add Links youtube https://youtube.com)"
                                )

        #  Add the initialized feature here
        features = [greeting_feature, get_help_feature, add_event_feature, note_feature]

        return features


    async def greet(self):
        await self.message.channel.send(f"Hi {self.message.author}! I am Sr.Engenheiro\nWould you like some assistance today?")
        return


    async def add_event(self, event_name, event_date):
        events = {}
        events[event_name] = event_date
        await self.message.channel.send(f"I'll add it to the list.")
        return


    async def get_help(self):
        text = ""
        features = self.get_Features()
        for feature in features:
            text += feature.description + "\n"
        
        await self.message.channel.send(text)
        return


    async def note(self, action, topic, name=None, item=None):
        action = action.upper()
        topic = topic.upper()
        

        if action == "ADD":
            name = name.upper()
            record = {name: item}
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

                #  In case the name doesnt exist in the topic
                try:
                    record = records[name]
                except KeyError:
                    await self.message.channel.send(f"Sorry, I have no record of {name} in the topic {topic}.")
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
            await self.message.channel.send(f"{name} removed from {topic}.")
            return
        
        else:
            await self.message.channel.send(f"I don't know how to perform action {action} :(")
            return