from datetime import date


def get_Commands(command):
    entries = command.split("\n")
    command = entries.pop(0)[1:]
    
    #  Multiple entry commands
    if len(entries) > 1:
        items = []
        for item in entries:
            if item.endswith('"'):
                item = split_quotes(item)
            else:
                item = item[0].split(" ")
            items.append(item)
        command = command.split(" ")
        command.append(items)

    else:
        #  If there is quote text
        if command.endswith('"'):
            command = split_quotes(command)
        else:
            command = command.split(" ")

        if command == []:
            return ["hi"]

    return command


def split_quotes(command):
    command = command.split('"')
    quote_text = command[1]
    command = command[0].split(" ")[:-1]
    command.append(quote_text)
    return command


def get_Args(commands, feature, records, message):
    params = []
    if feature.args_required:
        arguments = [commands[i+1] for i in range(len(commands)-1)]
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