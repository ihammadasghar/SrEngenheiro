from datetime import date


def get_Commands(command):
    parts = command.split("\n")
    commands =  parts[0].split('"')
    if len(commands) == 3:
        quotes_text = commands[1]
        commands = commands[0].split(" ")
        commands.pop()
        commands.append(quotes_text)
    else:
        commands = commands[0].split(" ")

    if len(commands) < 2:
        return ["sr!", "hi"]
    
    if len(parts) > 1:
        items = []
        for item in parts[1:]:
            item = item.split('"')
            if len(item) == 3:
                quotes_text = item[1]
                item = item[0].split(" ")
                item.pop()
                item.append(quotes_text)
            else:
                item = item[0].split(" ")
            items.append(item)
        commands.append(items)

    return commands


def get_Args(commands, feature, records, message):
    params = []
    if feature.args_required:
        arguments = [commands[i+2] for i in range(len(commands)-2)]
        params.append(arguments)

    if feature.records_Required:
        params.append(records)

    if feature.message_Required:
        params.append(message)

    return params


def get_Days_Left(event_Date):
    date_Today = date.today()
    date_Today = date_Today.strftime("%d/%m/%Y")
    date_Today = date_Today.split("/")
    date_Today = list(map(int, date_Today))
    date_Today = date(date_Today[2], date_Today[1], date_Today[0])
    event_Date = event_Date.split("/")
    event_Date = list(map(int, event_Date))
    event_Date = date(event_Date[2], event_Date[1], event_Date[0])
    return (event_Date-date_Today).days