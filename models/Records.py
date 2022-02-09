class Records:
    def __init__(self, data_Messages, data_Channel) -> None:
        self.data_Messages = data_Messages
        self.data_Channel = data_Channel
    

    def get_Message(self, topic):
        for message in self.data_Messages:
            if message.content.startswith(topic):
                return message 
        return None


    def get(self, topic, record_Message=None):
        if record_Message is None:
            record_Message = self.get_Message(topic)

        #  If record doesn't exist
        if not record_Message:
            return None
        
        record = record_Message.content.split("\n")[1:]

        records_List = []
        for item in record:
            item = item.split(" ")
            records_List.append({"name": item[0], "item": item[1]})
        
        return records_List


    async def update(self, topic, records):
        record_Message = self.get_Message(topic)
        new_Record = f"{topic}"

        for record in records:
                new_Record += "\n" + record["name"] + " " + record["item"]
        
        if record_Message is None:
            await self.data_Channel.send(new_Record)
            return

        await record_Message.edit(content=new_Record)
        return


    async def add(self, topic, records):
        old_Records = self.get(topic)
        if not old_Records is None:
            records = old_Records + records
        await self.update(topic, records)

    

    async def remove(self, topic, record_Name):
        records = self.get(topic)

        #  If record doesn't exist
        if not records:
            return False
        
        for record in records:
            if record["name"] == record_Name:
                records.remove(record)
                await self.update(topic, records)
                return True
        #  Record not found
        return False