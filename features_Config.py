from models.Feature import Feature
from views.response import *
from settings import ACTIVATION_SYMBOL

#  Intialize your feature here
greeting_feature =  Feature(command="HI", 
                            view_Function=greet, 
                            description=None,
                            message_Required=True
                            )

current_day_feature = Feature(command="TODAY",
                              view_Function=today,
                              description=f"**-> Date today**: `{ACTIVATION_SYMBOL}sr today`"
                              )               

praise_feature = Feature(command="GOOD-BOT",
                        view_Function=praise,
                        description=f"**-> Praise**: `{ACTIVATION_SYMBOL}sr Good-Bot`"
                        )

scold_feature = Feature(command="BAD-BOT",
                        view_Function=scold,
                        description=f"**-> Scold**: `{ACTIVATION_SYMBOL}sr Bad-Bot`"
                        )

    
help_feature = Feature(command="HELP", 
                      view_Function=help,
                      description= f"**-> Help**: `{ACTIVATION_SYMBOL}sr help`"
                      )

add_description = f"""**-> Add:**
 - `{ACTIVATION_SYMBOL}add note [tag] "[content]"`
 - `{ACTIVATION_SYMBOL}add note [topic] [tag] "[content]"`
 - `{ACTIVATION_SYMBOL}add event [topic] [tag] [Day/Month/Year]` or
```{ACTIVATION_SYMBOL}add event/note [topic]
[tag] [(Day/Month/Year)/content]
[tag] [(Day/Month/Year)/content]```"""
add_feature = Feature(command="ADD", 
                      args_required=True, 
                      view_Function=add, 
                      records_Required=True,
                      description=add_description
                      )

edit_description = f"""**-> Edit:**
 - `{ACTIVATION_SYMBOL}edit note [tag] "[content]"`
 - `{ACTIVATION_SYMBOL}edit note [topic] [tag] "[content]"`
 - `{ACTIVATION_SYMBOL}edit event [topic] [tag] [Day/Month/Year]`"""
edit_feature = Feature(command="EDIT", 
                      args_required=True, 
                      view_Function=edit, 
                      records_Required=True,
                      description=edit_description
                      )

remember_message_feature = Feature(command="REMEMBER",
                                  args_required=True,
                                  records_Required=True,
                                  message_Required=True,
                                  view_Function=remember_Message,
                                  description=f"**-> Remember messages**: `{ACTIVATION_SYMBOL}remember [tag]`(reply to the message)"
                                  )

forget_description = f"""**-> Forget:** `{ACTIVATION_SYMBOL}forget [message_tag]`
 - `{ACTIVATION_SYMBOL}forget note [tag]`
 - `{ACTIVATION_SYMBOL}forget note [topic] [tag(optional)]`
 - `{ACTIVATION_SYMBOL}forget event [topic] [tag(optional)]`"""
forget_feature = Feature(command="FORGET",
                        args_required=True,
                        records_Required=True,
                        view_Function=forget,
                        description=forget_description
                        )

get_description = f"""**-> Get:** `{ACTIVATION_SYMBOL}get [message_tag]`
 - `{ACTIVATION_SYMBOL}get note [tag]`
 - `{ACTIVATION_SYMBOL}get note [topic] [tag(optional)]`
 - `{ACTIVATION_SYMBOL}get event [topic] [tag(optional)]`"""
get_feature = Feature(command="GET",
                      args_required=True,
                      records_Required=True,
                      view_Function=get,
                      description=get_description
                      )

events_description =f"""**-> Events:** `{ACTIVATION_SYMBOL}events`
 - `{ACTIVATION_SYMBOL}events urgent`
 - `{ACTIVATION_SYMBOL}events topics`"""
events_feature = Feature(command="EVENTS", 
                        args_required=True, 
                        view_Function=events, 
                        records_Required=True,
                        description=events_description
                        )

notes_feature = Feature(command="NOTES", 
                        args_required=True, 
                        view_Function=notes,
                        records_Required=True, 
                        description=f"**-> Note topics:** `{ACTIVATION_SYMBOL}notes`"
                        )

messages_feature = Feature(command="MESSAGES", 
                        args_required=True, 
                        view_Function=messages,
                        records_Required=True, 
                        description=f"**-> Remembered Messages:** `{ACTIVATION_SYMBOL}messages`"
                        )


#  Add the initialized feature here
features = [greeting_feature,
            praise_feature, 
            scold_feature,  
            help_feature, 
            current_day_feature, 
            events_feature, 
            notes_feature, 
            remember_message_feature,
            messages_feature,
            add_feature, 
            get_feature,
            edit_feature, 
            forget_feature,
            ]





