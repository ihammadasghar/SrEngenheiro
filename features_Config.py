from models.Feature import Feature
from views.response import *

#  Intialize your feature here
greeting_feature =  Feature(command="HI", 
                            view_Function=greet, 
                            description="**-> Hi**: `sr! hi`",
                            message_Required=True
                            )

current_day_feature = Feature(command="TODAY",
                            view_Function=today,
                            description="**-> Date today**: `sr! today`"
                            )               

praise_feature = Feature(command="GOOD-BOT",
                            view_Function=praise,
                            description="**-> Praise**: `sr! Good-Bot`"
                            )

scold_feature = Feature(command="BAD-BOT",
                            view_Function=scold,
                            description="**-> Scold**: `sr! Bad-Bot`"
                            )

    
help_feature = Feature(command="HELP", 
                            view_Function=help,
                            description="**-> Help**: `sr help`"
                            )

events_description ="""**-> Events:**
 - Schedule: `sr! events`
 - Urgent: `sr! events urgent`
 - Topics: `sr! events topics`
 - Add/Edit:`sr! events [add/edit] [topic] [name] [Day/Month/Year]`
 - Multiple events:
```sr! events [add/edit] [topic]
[name] [Day/Month/Year]
[name] [Day/Month/Year]```
 - Get/Delete: `sr! events [get/delete] [topic] [name(optional)]`"""
events_feature = Feature(command="EVENTS", 
                            args_required=True, 
                            view_Function=events, 
                            records_Required=True,
                            description=events_description
                          )

notes_description = """**-> Notes:**
 - Topics: `sr! notes` 
 - Add/Edit: `sr! notes [add/edit] [topic] [name] [item]`
 - Multiple notes:
```sr! notes [add/edit] [topic]
[name] "[content]"
[name] "[content]"```
 - Get/Delete: `sr! notes [get/delete] [topic] [name(optional)]`"""
notes_feature = Feature(command="NOTES", 
                        args_required=True, 
                        view_Function=notes,
                        records_Required=True, 
                        description=notes_description
                        )

remember_feature = Feature(command="REMEMBER",
                            args_required=True,
                            records_Required=True,
                            message_Required=True,
                            view_Function=remember_Message,
                            description="**-> Remember messages/files**: `sr! remember [name]`(reply to the message)"
                            )

forget_feature = Feature(command="FORGET",
                            args_required=True,
                            records_Required=True,
                            view_Function=forget_Message,
                            description="**-> Forget messages/files**: `sr! forget [name]`"
                            )

get_message_feature = Feature(command="GET",
                            args_required=True,
                            records_Required=True,
                            view_Function=get_Message,
                            description="**-> Get messages/files**: `sr! get [name]`"
                            )

#  Add the initialized feature here
features = [greeting_feature, current_day_feature, praise_feature, scold_feature, help_feature, events_feature, notes_feature, get_message_feature, remember_feature, forget_feature]





