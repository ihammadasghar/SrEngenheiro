class Feature:
    def __init__(self, command, args, functionality, server_Record_Required=False, description="No description") -> None:
        self.command = command
        self.args = args
        self.functionality = functionality
        self.description = description