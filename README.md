# SrEngenheiro
Sr.Engenheiro is a Discord Bot designed by a team of Computer Science students in Universidade Autónoma de Lisboa with the goal to assist various Student/Faculty Discord Servers.


## How to contribute a new feature:
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
