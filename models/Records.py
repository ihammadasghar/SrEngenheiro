class Records:
    def __init__(self, records, server) -> None:
        self.records = records
        self.server = server
        self.updated = False


    def get(self, table=None, topic=None):
        try:
            if not table and not topic:
                return self.records

            elif table and not topic:
                return self.records[table]

            elif table and topic:
                return self.records[table][topic]

        except KeyError:
            return None

        return None


    def update(self, records, table=None, topic=None):
        old_Records = self.records

        if table:
            if not table in old_Records.keys():
                old_Records[table] = {}
            
            if not topic:
                old_Records[table].update(records)
            
            else:
                if not topic in old_Records[table].keys():
                    old_Records[table][topic] =  {}
                old_Records[table][topic].update(records)
        else:
            self.records = records

        self.updated = True
    

    def remove(self, table, topic=None, name=None):
        #  If record doesn't exist
        if self.records == {}:
            return False

        try:
            if name:
                self.records[table][topic].pop(name)
            elif topic:
                self.records[table].pop(topic)
            else:
                self.records.pop(table)
        except KeyError:
            return False
        
        self.updated = True
        return True