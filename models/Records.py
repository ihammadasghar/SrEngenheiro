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

    
    def create(self, table, topic, name, item):
        already_exists = self.exists(table, topic, name)
        if not already_exists:
            self.records[table][topic].update({name: item})
            self.updated = True
            return True
        return False
    

    def exists(self, table, topic=None, name=None):
        if table in self.records.keys():
            if topic:
                if topic in self.records[table].keys():
                    if name:
                        if name in self.records[table][topic].keys():
                            return True
                        return False
                    return True
                return False
            return True
        return False


    def update(self, table, topic=None, name=None, item=None,  records=None):
        if topic:
            exists = self.exist(table, topic)
            if exists:
                if name:
                    exists = self.exist(table, topic, name)
                    if exists:
                        self.records[table][topic][name] = item
                        self.updated = True
                        return True
                    return False
                self.records[table][topic].update(records)
                self.updated = True
                return True
            return False
        
        exist = self.exists(table)
        if exist:
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
            elif topic:
                self.records[table].pop(topic)
            else:
                self.records.pop(table)
        except KeyError:
            return False
        
        self.updated = True
        return True