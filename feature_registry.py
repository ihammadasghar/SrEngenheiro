from models.Feature import Feature
from views.response import *

#  Intialize your feature here
greeting_feature =  Feature(command="HI", 
                            args=0, 
                            functionality=greet, 
                            description="Hi: greetings!"
                            )

current_day_feature = Feature(command="TODAY",
                            args=0,
                            functionality=today,
                            description="TODAY: Tells the current date."
                            )               

praise_feature = Feature(command="GOOD-BOT",
                            args=0, 
                            functionality=praise,
                            description="PRAISE: ???."
                            )
    
help_feature = Feature(command="HELP", 
                            args=0, 
                            functionality=help,
                            description="HELP: Lists all commands."
                            )

events_feature = Feature(command="EVENTS", 
                            args=[2, 3, 4], 
                            functionality=events, 
                            description="EVENTS [action] [topic] [name] [date]: Adds events (e.g. event add Testes AP 22/4/2022)\n Possible Actions:\n  - Add\n  - Delete\n  - Get"
                            )

notes_feature = Feature(command="NOTES", 
                        args=[2, 3, 4], 
                        functionality=notes,
                        records_Required=True, 
                        description="NOTES [action] [topic] [name] [item]: Makes notes (e.g. notes add Links youtube https://youtube.com)\n  Possible Actions:\n  - Add\n  - Delete\n  - Get"
                        )

#  Add the initialized feature here
features = [greeting_feature, current_day_feature, praise_feature, help_feature, events_feature, notes_feature]
