class Feature:
    def __init__(self, command, args, functionality, description="No description", records_Required=False, message_Required=False) -> None:
        self.command = command
        self.args = args
        self.functionality = functionality
        self.description = description
        self.records_Required = records_Required
        self.message_Required = message_Required