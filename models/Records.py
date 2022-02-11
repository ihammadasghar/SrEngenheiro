from discord import File
import pickle


class Records:
    def __init__(self, data_Messages, data_Channel, server_ID) -> None:
        self.data_Messages = data_Messages
        self.data_Channel = data_Channel
        self.server_ID = server_ID

    def get_Message(self):
        for message in self.data_Messages:
            if message.content.startswith(self.server_ID):
                return message
                
        return None


    def get(self, table=None, topic=None, record_Message=None):
        if record_Message is None:
            record_Message = self.get_Message()

        #  If record doesn't exist
        if not record_Message:
            return None
        
        data = pickle.load(record_Message.attachments[0])

        if not table and not topic:
            return data["records"]

        elif table and not topic:
            return data["records"][table]

        elif table and topic:
            return data["records"][table][topic]

        return None


    async def update(self, records, table=None, topic=None):
        record_Message = self.get_Message()
        data = self.get()

        if not table and not topic:
            data["records"] = records

        elif table and not topic:
            data["records"][table] = records

        elif table and topic:
            data["records"][table][topic] = records
        
        data["Server_ID"] = self.server_ID

        filepath = f"./{self.server_ID}"
        with open(filepath, mode="w") as file:
            pickle.dump(data, file)

        file = File(filepath)
        if record_Message is None:
            await record_Message.send(content=self.server_ID, file=file)
            return

        await record_Message.edit(content=self.server_ID, file=file)
        return


    async def add(self, records, table=None, topic=None):
        old_Records = self.get(table, topic)

        if not old_Records is None:
            if not table and not topic:
                records.update(old_Records["records"])

            elif table and not topic:
                records.update(old_Records["records"][table])

            elif table and topic:
                records.update(old_Records["records"][table][topic])

        await self.update(table, topic, records)

    

    async def remove(self, table, topic=None, name=None):
        records = self.get(table, topic)

        #  If record doesn't exist
        if not records:
            return False
        
        records.pop(name)
        if not topic and not name:
            try:
                records.pop(table)
            except KeyError:
                return False

        elif topic and not name:
            try:
                records.pop(topic)
            except KeyError:
                return False

        elif topic and name:
            try:
                records.pop(name)
            except KeyError:
                return False
        
        await self.update(table, topic, records)
        return True