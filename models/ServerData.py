class ServerData:
    def __init__(self, data, channel) -> None:
        self.data = data
        self.channel = channel
    
    def filter_data(self, data_tag):
        for message in self.data:
            if message.startswith(data_tag):
                return message 
        return None