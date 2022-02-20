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
    date_Today = to_Date(date_Today)

    event_Date = to_Date(event_Date)

    return (event_Date-date_Today).days


def to_Date(date_string):
    date_string = date_string.split("/")
    date_string = list(map(int, date_string))
    date_object = date(date_string[2], date_string[1], date_string[0])
    return date_object


def is_Correct_Date_Format(date):
    date = date.split("/")
    if len(date) == 3 and int(date[0])<=31 and int(date[1])<=12 and int(date[2])>0:
        return True
    return False