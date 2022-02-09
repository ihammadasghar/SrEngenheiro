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

        record_dict = {}
        for item in record:
            item = item.split(" ")
            record_dict.update({item[0]: item[1]})
        
        return record_dict


    async def update(self, topic, records):
        record_Message = self.get_Message(topic)
        new_Record = f"{topic}"

        for item in records.items():
                new_Record += "\n" + item[0] + " " + item[1]
        
        await record_Message.edit(content=new_Record)
        return


    async def add(self, topic, records):
        record_Message = self.get_Message(topic)

        #  If no previous record of the record type
        if record_Message is None:
            result = topic
            for record in records.items():
                result += "\n" + record[0] + " " + record[1]
            await self.data_Channel.send(result)
            return
        
        old_records = self.get(topic)
        old_records.update(records)
        await self.update(topic, old_records)

    

    async def remove(self, topic, record_Key):
        records = self.get(topic)

        #  If record doesn't exist
        if not records:
            return False
        
        try:
            records.pop(record_Key)
        except KeyError:
            return False

        await self.update(topic, records)
        return True