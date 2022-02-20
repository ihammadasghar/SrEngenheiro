from models.Feature import Feature
from views.response import *
from settings import ACTIVATION_WORD

#  Intialize your feature here
greeting_feature =  Feature(command="HI", 
                            view_Function=greet, 
                            description=f"**-> Hi**: `{ACTIVATION_WORD} hi`",
                            message_Required=True
                            )

current_day_feature = Feature(command="TODAY",
                              view_Function=today,
                              description=f"**-> Date today**: `{ACTIVATION_WORD} today`"
                              )               

praise_feature = Feature(command="GOOD-BOT",
                        view_Function=praise,
                        description=f"**-> Praise**: `{ACTIVATION_WORD} Good-Bot`"
                        )

scold_feature = Feature(command="BAD-BOT",
                        view_Function=scold,
                        description=f"**-> Scold**: `{ACTIVATION_WORD} Bad-Bot`"
                        )

    
help_feature = Feature(command="HELP", 
                      view_Function=help,
                      description="**-> Help**: `sr help`"
                      )

add_description = f"""**-> Add:**
 - `{ACTIVATION_WORD} add note [topic] [note_name] "[content]"`
 - `{ACTIVATION_WORD} add event [topic] [event_name] [Day/Month/Year]`
 - To add/edit multiple at once notes/events use the following format:
```{ACTIVATION_WORD} add event [topic]
[name] [Day/Month/Year]
[name] [Day/Month/Year]```"""
add_feature = Feature(command="ADD", 
                      args_required=True, 
                      view_Function=add, 
                      records_Required=True,
                      description=add_description
                      )

edit_description = f"""**-> Edit:**
 - `{ACTIVATION_WORD} edit note [topic] [note_name] "[content]"`
 - `{ACTIVATION_WORD} edit event [topic] [event_name] [Day/Month/Year]`"""
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
                                  description=f"**-> Remember messages**: `{ACTIVATION_WORD} remember [name]`(reply to the message)"
                                  )

forget_description = f"""**-> Forget:**
 - `{ACTIVATION_WORD} forget [message_name]`
 - `{ACTIVATION_WORD} forget note [topic] [name(optional)]`
 - `{ACTIVATION_WORD} forget event [topic] [name(optional)]`"""
forget_feature = Feature(command="FORGET",
                        args_required=True,
                        records_Required=True,
                        view_Function=forget,
                        description=forget_description
                        )

get_description = f"""**-> Get:**
 - `{ACTIVATION_WORD} get [message_name]`
 - `{ACTIVATION_WORD} get note [topic] [name(optional)]`
 - `{ACTIVATION_WORD} get event [topic] [name(optional)]`"""
get_feature = Feature(command="GET",
                      args_required=True,
                      records_Required=True,
                      view_Function=get,
                      description=get_description
                      )

events_description =f"""**-> Events:**
 - Schedule: `{ACTIVATION_WORD} events`
 - Urgent: `{ACTIVATION_WORD} events urgent`
 - Topics: `{ACTIVATION_WORD} events topics`"""
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
                        description=f"**-> Note topics:** `{ACTIVATION_WORD} notes`"
                        )


#  Add the initialized feature here
features = [greeting_feature,
            current_day_feature, 
            praise_feature, 
            scold_feature, 
            help_feature, 
            remember_message_feature,
            add_feature, 
            get_feature,
            edit_feature, 
            forget_feature,
            events_feature, 
            notes_feature,  
            ]





