class Feature:
    def __init__(self, command, view_Function, description="No description", records_Required=False, message_Required=False, args_required=False) -> None:
        self.command = command
        self.args_required = args_required
        self.view_Function = view_Function
        self.description = description
        self.records_Required = records_Required
        self.message_Required = message_Required