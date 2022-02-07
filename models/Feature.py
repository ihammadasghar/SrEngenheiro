class Feature:
    def __init__(self, command, args, functionality, data_required=False, description="No description") -> None:
        self.command = command
        self.args = args
        self.functionality = functionality
        self.data_required = data_required
        self.description = description