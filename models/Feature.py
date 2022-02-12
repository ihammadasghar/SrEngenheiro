class Feature:
    def __init__(self, command, nargs, view_Function, description="No description", records_Required=False, message_Required=False) -> None:
        self.command = command
        self.nargs = nargs
        self.view_Function = view_Function
        self.description = description
        self.records_Required = records_Required
        self.message_Required = message_Required