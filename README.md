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

3. In FeatureController.py initialize an instance of the Feature model in the get_Features function 
```
feature_name = Feature("feature_command", number_of_arguments, feature_function)
```

4. Add the intialized feature to the features list at the bottom of the get_features function.

5. Define your function at the bottom on the FeatureController.py
```
async def feature_function(message):
    #  Your code here
```

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
#  Create a dictionary of your data.
link_Records = {
    "youtube": "https://youtube.com",
    "facebook": "https://facebook.com"
    }

#  Pass the dictionary to the function to save and the topic/table name
await self.records.add(topic="Links", records=link_Records)
```

### Getting records:
```
#  Getting one record
#  Pass the topic/table name and record key.
youtube_Link_Record = self.records.get(topic="Links", record_Key="youtube")

#  Getting all records about a topic
#  Pass the topic/table name.
all_Link_Records = self.records.get(topic="Links")
```

### Removing records:
```
#  Removing link youtube from the Links topic.
await self.records.remove(topic="Links", record_Key="youtube")

```