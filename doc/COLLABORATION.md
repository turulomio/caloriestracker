# Collaboration procedure

Companies, products and its formats are hardcoded in this app and it's only updated by new releases. Nevertheless you can add your own personal companies, products and formats, as you with.

If your data information has enough quality, it's in English and if you wish to share your personal products of your database to convert them in system ones, you have to execute this command:

`caloriestracker_console --contribution_dump`

Perhaps you'll need to add some Postgres connection parameters use `caloriestracker_console --help` for help

You'll get a file named like `caloriestracker_collaboration_201909272007.sql`, please send it to me to turulomio@yahoo.es

I'll parse your file and I will generate a new Calories Trackerversion with your data. 

I'll send you a file with a name similar to '201910272018_version_needed_update_first_in_github.sql'. You need to update CaloriesTracker to the last version and then run this command:

`caloriestracker_console --update_after_contribution 201910272018_version_needed_update_first_in_github.sql `