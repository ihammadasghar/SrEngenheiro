class Records:
    def __init__(self, records, server) -> None:
        self.records = records
        self.server = server
        self.updated = False
        self.requested_message_ID = None


    def get(self, table, topic=None, name=None):
        try:
            if name:
                return self.records[table][topic][name]
            elif topic:
                return self.records[table][topic]

            return self.records[table]

        except KeyError:
            return None

    
    def create(self, table, topic, name, item):
        already_existing_record = self.get(table, topic, name)
        if already_existing_record is None:
            existing_table = self.get(table)
            if existing_table is None:
                self.records[table] = {}
                
            existing_topic = self.get(table, topic)
            if existing_topic is None:
                self.records[table][topic] = {}
                
            self.records[table][topic].update({name: item})
            self.updated = True
            return True
        return False


    def update(self, table, topic=None, name=None, item=None, records=None):
        if topic:
            existing_record = self.get(table, topic)
            if existing_record:
                if name:
                    existing_record = self.get(table, topic, name)
                    if existing_record:
                        self.records[table][topic][name] = item
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
    

    def remove(self, table, topic=None, name=None):
        #  If record doesn't exist
        if self.records == {}:
            return False

        try:
            if name:
                self.records[table][topic].pop(name)
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