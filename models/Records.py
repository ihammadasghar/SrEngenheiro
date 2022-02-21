class Records:
    def __init__(self, records, server) -> None:
        self.records = records
        self.server = server
        self.updated = False
        self.requested_message_ID = None


    def get(self, table, topic=None, tag=None):
        try:
            if tag:
                return self.records[table][topic][tag]
            elif topic:
                return self.records[table][topic]

            return self.records[table]

        except KeyError:
            return None

    
    def create(self, table, topic, tag, content):
        already_existing_record = self.get(table, topic, tag)
        if already_existing_record is None:
            existing_table = self.get(table)
            if existing_table is None:
                self.records[table] = {}
                
            existing_topic = self.get(table, topic)
            if existing_topic is None:
                self.records[table][topic] = {}
                
            self.records[table][topic].update({tag: content})
            self.updated = True
            return True
        return False


    def update(self, table, topic=None, tag=None, content=None, records=None):
        if topic:
            existing_record = self.get(table, topic)
            if existing_record:
                if tag:
                    existing_record = self.get(table, topic, tag)
                    if existing_record:
                        self.records[table][topic][tag] = content
                        self.updated = True
                        return True
                    return False
                self.records[table][topic].update(records)
                self.updated = True
                return True
            return False
        
        existing_record = self.get(table)
        if existing_record:
            self.records[table].update(records)
            self.updated = True
            return True
        return False
    

    def remove(self, table, topic=None, tag=None):
        #  If record doesn't exist
        if self.records == {}:
            return False

        try:
            if tag:
                self.records[table][topic].pop(tag)
                if self.records[table][topic] == {}:
                    self.records[table].pop(topic)
            elif topic:
                self.records[table].pop(topic)
            else:
                self.records.pop(table)
        except KeyError:
            return False
        
        self.updated = True
        return True