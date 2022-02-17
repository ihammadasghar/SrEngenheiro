from models.Feature import Feature
from views.response import *

#  Intialize your feature here
greeting_feature =  Feature(command="HI", 
                            view_Function=greet, 
                            description="**-> Hi**\n```sr! hi```",
                            message_Required=True
                            )

current_day_feature = Feature(command="TODAY",
                            view_Function=today,
                            description="**-> Date today**\n```sr! today```"
                            )               

praise_feature = Feature(command="GOOD-BOT",
                            view_Function=praise,
                            description="**-> Praise**\n```sr! Good-Bot```"
                            )

scold_feature = Feature(command="BAD-BOT",
                            view_Function=scold,
                            description="**-> Scold**\n```sr! Bad-Bot```"
                            )

    
help_feature = Feature(command="HELP", 
                            view_Function=help,
                            description="**-> Help**\n```sr help```"
                            )

events_feature = Feature(command="EVENTS", 
                            args_required=True, 
                            view_Function=events, 
                            records_Required=True,
                            description="""**-> Events**\n
```sr! events [add/edit/get/delete] [topic] [name] [Day/Month/Year]\n
sr! events Add Tests Math 22/4/2022```\n-> Events in the next 7 days\n
```sr! events urgent```\nAdding multiple events\n
```sr! events Add Tests\nMath 22/4/2022\nEnglish 21/4/2022```"""
                          )

notes_feature = Feature(command="NOTES", 
                        args_required=True, 
                        view_Function=notes,
                        records_Required=True, 
                        description="""**-> Notes**\n
```sr! notes [add/edit/get/delete] [topic] [name] [item]\n
sr! notes add Gods Thor "The strongest!"```\n
Adding multiple notes\n```sr! notes add Gods\n
Zeus "Thunder innit"\nAries "The god of war"```"""
                        )

#  Add the initialized feature here
features = [greeting_feature, current_day_feature, praise_feature, scold_feature, help_feature, events_feature, notes_feature]





