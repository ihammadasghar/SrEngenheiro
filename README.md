# SrEngenheiro
Sr.Engenheiro is a Discord Bot designed by a team of Computer Science students in Universidade Autónoma de Lisboa with the goal to assist various Student/Faculty Discord Servers.

## Topics:
- [How to contribute](#How-to-contribute)
- [How to use data/records module](#Using-Records-module)
    - [Adding records](#Adding-records:)
    - [Getting records](#Getting-records:)
    - [Removing records](#Removing-records:)

## How to contribute:
NOTE: To run the bot you need .env file avaibable on Discord server in your local clone.

1. Clone the Repository
```
git clone https://github.com/ihammadasghar/SrEngenheiro.git
```
cd to SrEngenheiro and dowload all the required packages/libraries:
```
pip install -r requirements.txt
```

2. Make a new branch with the your feature name (e.g. "git branch greeting_feature")
```
git checkout -b featurename_feature
```

3. In feature_Config.py create an instance of the Feature model
- command: (str) Should be in all caps
- nargs: (int) number of arguments
- view_Function: (function refrence) Corresponding view function.
```
feature_name = Feature(command, nargs, view_Function, description="No description", records_Required=False, message_Required=False)
```

4. Add the instantiated feature to the features list at the bottom

5. Define your view function in views/response.py at the bottom.
- args: (list) a list of all arguments of the command
- records: (records) [records module](#Using-Records-module) with function update,get,remove
- message: (message) command message object
```
def featurename(args, records, message):
    #  Your code here
    date_Today = fclr.get_Date_Today()  #  fclr is the feature controller
    response = f"Date today is {date_Today}"
    return response
```
NOTE: All arguments validation and response string generation should be done in the view function while all the data fetching and processing (i.e. technical stuff) should be defined in FeatureController.py
 
6. Add and Commit
```
git add .
git commit -m "what changes you made"
```

7. Push your branch.
```
git push origin branch_name
```

8. Go to github there will be a notification to "create a Pull request", add a description of the functionality of your feature for others to understand what you did and post the pull request.

## Using Records module
### Adding records:
```
#  Create a dictionaries of your data.
link_Record = {"youtube": "https://youtube.com"}

#  Pass the dictionary to the function to save and the topic and table name
records.add(table="NOTES", topic="Links", records=link_Record)
```

### Getting records:
```
#  Getting one record
youtube_Link_Record = self.records.get(table="NOTES", topic="Links", record_Name="youtube")

#  Getting a list of all records about a topic
all_Link_Records = records.get(table="NOTES", topic="Links")
```

### Removing records:
```
#  Removing link youtube from the Links topic.
records.remove(table="NOTES", topic="Links", record_Name="youtube")

```
