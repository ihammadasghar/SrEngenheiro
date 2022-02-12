class Feature:
    def __init__(self, command, args, functionality, records_Required=False, description="No description") -> None:
        self.command = command
        self.args = args
        self.functionality = functionality
        self.description = description
        self.records_Required = records_Required