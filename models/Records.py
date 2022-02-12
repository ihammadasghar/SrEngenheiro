from discord import File
import pickle
from os import remove as delete_file


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


    async def get(self, table=None, topic=None, record_Message=None):
        if record_Message is None:
            record_Message = self.get_Message()

        #  If record doesn't exist
        if not record_Message:
            return None
        
        file = await record_Message.attachments[0].to_file()
        file = file.fp

        data = pickle.load(file)

        if not table and not topic:
            return data["Records"]

        elif table and not topic:
            return data["Records"][table]

        elif table and topic:
            return data["Records"][table][topic]

        return None


    async def update(self, records, table=None, topic=None):
        record_Message = self.get_Message()
        old_Records = await self.get()
        if not old_Records:
            print(f"No existing records...\nInitialized empty records dictionary.")
            old_Records = {}

        print(f"Records: {old_Records}")

        if not table and not topic:
            print(f"Updating records...")
            old_Records.update(records)

        elif table and not topic:
            print(f"Request to update table {table}...")

            if table not in old_Records.keys():
                print(f"Table {table} not found...")
                print(f"Created new empty table {table}...")
                old_Records[table] = {}

            print(f"Updating table {table}...")
            old_Records[table].update(records)

        elif table and topic:
            print(f"Request to update topic {topic} in table {table}...")
            if table not in old_Records.keys():
                print(f"Table {table} not found...")
                old_Records[table] = {}

            if topic not in old_Records[table].keys():
                print(f"Topic {topic} not found in table {table}...")
                print(f"Creating new empty topic {topic} in table {table}...")

                old_Records[table][topic] = {}

            print(f"Updating topic {topic} in table {table}...")
            old_Records[table][topic].update(records)
        
        data = {}
        data["Server_ID"] = self.server_ID
        data["Records"] = old_Records

        filepath = f"./{self.server_ID}"
        with open(filepath, mode="wb") as file:
            pickle.dump(data, file)

        file = File(filepath)
        if record_Message:
            await record_Message.delete()

        await self.data_Channel.send(content=self.server_ID, file=file)

        delete_file(filepath)

        print("Records update succesfull.")
        return


    async def add(self, records, table=None, topic=None):
        old_Records = await self.get(table=table, topic=topic)

        if old_Records:
            if not table and not topic:
                print(f"Request to add tables to records.\nTables: {records}")
                old_Records.update(records)

            elif table and not topic:
                print(f"Request to add topics table {table}.\nTopics: {records}")
                old_Records[table].update(records)

            elif table and topic:
                print(f"Request to add entries to topic {topic} in table {table}.\nEntries: {records}")
                old_Records[table][topic].update(records)

            await self.update(table=table, topic=topic, records=old_Records)
            return
        await self.update(table=table, topic=topic, records=records)
        

    

    async def remove(self, table, topic=None, name=None):
        records = await self.get(table=table)

        #  If record doesn't exist
        if not records:
            print("No existing records.")
            return False

        print(f"Records: {records}")

        if not topic and not name:
            try:
                print(f"Deleting table {table}...")
                records.pop(table)
            except KeyError:
                print(f"Table {table} not found.")
                return False

        elif topic and not name:
            try:
                print(f"Deleting topic {topic} from table {table}...")
                records.pop(topic)
            except KeyError:
                print(f"Topic {topic} not found in table {table}.")
                return False

        elif topic and name:
            try:
                print(f"Deleting entry {name} from topic {topic} in table {table}...")
                records[topic].pop(name)
            except KeyError:
                print(f"Entry {name} not found in topic {topic} of table {table}.")
                return False
        
        await self.update(table=table, records=records)
        return True