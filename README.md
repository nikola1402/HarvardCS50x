# Dungeon Master's Toolbox
#### Video Demo: https://youtu.be/2iFft3KGQGk
## Overview
This project aims to deliver a useful set of tools for Dungeon Masters hosting their Dungeons and Dragons sessions.

It is developed using Python, Django, Bootstrap, SQLite3 and [Open5e API for DnD SRD content](https://open5e.com/).


## Features
When opening the home page of this tool, the user is presented with the option to select the desired tool which they would like to use.
### Encounter Generator
Encounter generator is a tool which helps Dungeon Masters with creating encounters for their parties.

User has the following options:
* Selection of party level
* Selection of party size
* Selection of difficulty

There are 4 levels of difficulty: easy, medium, hard and deadly.
If the user is unsure which level of difficulty to apply, there is a short descriptive text for each of the choices.

Clicking on button 'Generate encounter', this tool will provide a table of DnD monsters which need to be included for that section of the game.
Table includes the following data which may be helpful:
* Name of the monster
* Armor Class
* Health Points
* Challenge Rating

Alongside this, user is notified about chosen difficulty and total XP that is gained from successfully completing the encounter.

### Hit and Fumble Tables
Dungeon Masters may want to add flavor, randomness, and narrative impact to critical successes or failures during gameplay.
Hit and Fumble tables are part of optional rules and mechanics that enable this addition to the game.
Tool provided here gives users access to this fun part of the game.

There are 2 parts of this tool:
1. Hit and Fumble tables which users that like to use physical dice can use as a reference during their gameplay.
2. Application for rolling quickly on these tables online, using online dice.

There are 4 tables in total presented to the user:
1. Weapon Hit table
2. Weapon Fumble table
3. Spell Hit table
4. Spell Fumble table

Each table contains the following:
* Range of numbers rolled on the dice for which this effect applies
* Description of the effect, which helps the narrative and flavor of the encounter
* Actual effect on the gameplay

If the user want to use the tool to roll the virtual dice, they are presented with options on which tables they would like to roll their dice on.
By clicking on the 'Roll' button, they are presented with their dice roll and new table which is generated based on their choices and the number that they have rolled. This table contains all the data that regular tables hold, with the addition of the name of the table to which the specific row corresponds to.

Another functionality here provides user with the ability to add their own tables to the application. By clicking on the button 'Add new table', user is redirected to a page where they need to provide a JSON file which contains all the required data. There is also an example on how the user should format their JSON file, and a short description of each of the fields.

## Project in depth
This project is a web app created with Django and other web programming technologies, aimed at players of Dungeons and Dragons.

### Controller
#### app.py
Main hub of this application is in **app.py**, which handles all the routing and forwards data to other parts of the application to be processed or presented.

When using 'Tables' tool, this file will provide the page four different input parameters:
1. _'data'_: All the data from database table 'hit_fumble', which will be presented as different tables on the webpage.
2. _'options'_: Attack types and options found in the database table, to be presented as form options for the user
3. _'rolled'_: Number that is rolled on the digital dice (0 if we still haven't rolled anything)
4. _'results'_: Results for the rolled number, based on form options, to be presented to the user

Another functionality inside the 'Tables' is the ability to upload a JSON file which will be imported to the database inside of the 'hit_fumble' table.

Handling encounters is also done here, where the application will take party level, party size and difficulty from the user form, provide that data to the **helpers.py** and receive the encounter and total_xp parameters in return.
These parameters are used to show the user the monsters which are included in the encounter, as well as the total xp earned from it.

#### helpers.py
This part of the application olds all the logic for data processing.

It handles working with database, where we are able to import a new database file and retrieve results from it based on different requests which include getting different actions, types and results that belong in certain ranges of data.
These actions also enable user to see provided tables, and to get results from them based on rolling the digital dice.

Data is managed by using SQLite3, and is provided by user freeWeemsy in [this Reddit post](https://www.reddit.com/r/DnDBehindTheScreen/comments/68pwms/dnd_5e_critical_hit_tables_and_fumble_tables/).


Second important part of this file handles encounter generator.
With provided parameters of party size, party level and encounter difficulty, application will do the following:
1. Calculate XP threshold which will be used to determine the content of the encounter.
2. Calculate monsters Challenge Ratings (CR) available for this encouner.
3. Use [Open5e API for DnD SRD content](https://open5e.com/) to retrieve the monsters based on calculated CR.
4. It will sort the monsters per CR.
5. It will generate encounter by adding one monster at a time until XP threshold is reached.

### Presentation
Presentation part of the application is done by using HTML, CSS, Jinja, and Bootstrap.

Folder 'templates' holds all the html pages included in this project.
Core of this implementation is in the **layout.html** file, which holds the template for all the other pages.

Jinja is used to provide a data communication layer between the Controller part and Presentation part.

Bootstrap is used to make the visual aspect of the application more appealing and standardized.

### Resources and links
**Database data**: [Reddit post by u/freeWeemsy](https://www.reddit.com/r/DnDBehindTheScreen/comments/68pwms/dnd_5e_critical_hit_tables_and_fumble_tables/)

**Monsters data**: [Open5e API for DnD SRD content](https://open5e.com/)

**Images**: Generated by using [Leonardo AI](https://app.leonardo.ai/)
# Dungeon Master's Toolbox
#### Video Demo: https://youtu.be/2iFft3KGQGk
## Overview
This project aims to deliver a useful set of tools for Dungeon Masters hosting their Dungeons and Dragons sessions.

It is developed using Python, Django, Bootstrap, SQLite3 and [Open5e API for DnD SRD content](https://open5e.com/).


## Features
When opening the home page of this tool, the user is presented with the option to select the desired tool which they would like to use.
### Encounter Generator
Encounter generator is a tool which helps Dungeon Masters with creating encounters for their parties.

User has the following options:
* Selection of party level
* Selection of party size
* Selection of difficulty

There are 4 levels of difficulty: easy, medium, hard and deadly.
If the user is unsure which level of difficulty to apply, there is a short descriptive text for each of the choices.

Clicking on button 'Generate encounter', this tool will provide a table of DnD monsters which need to be included for that section of the game.
Table includes the following data which may be helpful:
* Name of the monster
* Armor Class
* Health Points
* Challenge Rating

Alongside this, user is notified about chosen difficulty and total XP that is gained from successfully completing the encounter.

### Hit and Fumble Tables
Dungeon Masters may want to add flavor, randomness, and narrative impact to critical successes or failures during gameplay.
Hit and Fumble tables are part of optional rules and mechanics that enable this addition to the game.
Tool provided here gives users access to this fun part of the game.

There are 2 parts of this tool:
1. Hit and Fumble tables which users that like to use physical dice can use as a reference during their gameplay.
2. Application for rolling quickly on these tables online, using online dice.

There are 4 tables in total presented to the user:
1. Weapon Hit table
2. Weapon Fumble table
3. Spell Hit table
4. Spell Fumble table

Each table contains the following:
* Range of numbers rolled on the dice for which this effect applies
* Description of the effect, which helps the narrative and flavor of the encounter
* Actual effect on the gameplay

If the user want to use the tool to roll the virtual dice, they are presented with options on which tables they would like to roll their dice on.
By clicking on the 'Roll' button, they are presented with their dice roll and new table which is generated based on their choices and the number that they have rolled. This table contains all the data that regular tables hold, with the addition of the name of the table to which the specific row corresponds to.

Another functionality here provides user with the ability to add their own tables to the application. By clicking on the button 'Add new table', user is redirected to a page where they need to provide a JSON file which contains all the required data. There is also an example on how the user should format their JSON file, and a short description of each of the fields.

## Project in depth
This project is a web app created with Django and other web programming technologies, aimed at players of Dungeons and Dragons.

### Controller
#### app.py
Main hub of this application is in **app.py**, which handles all the routing and forwards data to other parts of the application to be processed or presented.

When using 'Tables' tool, this file will provide the page four different input parameters:
1. _'data'_: All the data from database table 'hit_fumble', which will be presented as different tables on the webpage.
2. _'options'_: Attack types and options found in the database table, to be presented as form options for the user
3. _'rolled'_: Number that is rolled on the digital dice (0 if we still haven't rolled anything)
4. _'results'_: Results for the rolled number, based on form options, to be presented to the user

Another functionality inside the 'Tables' is the ability to upload a JSON file which will be imported to the database inside of the 'hit_fumble' table.

Handling encounters is also done here, where the application will take party level, party size and difficulty from the user form, provide that data to the **helpers.py** and receive the encounter and total_xp parameters in return.
These parameters are used to show the user the monsters which are included in the encounter, as well as the total xp earned from it.

#### helpers.py
This part of the application olds all the logic for data processing.

It handles working with database, where we are able to import a new database file and retrieve results from it based on different requests which include getting different actions, types and results that belong in certain ranges of data.
These actions also enable user to see provided tables, and to get results from them based on rolling the digital dice.

Data is managed by using SQLite3, and is provided by user freeWeemsy in [this Reddit post](https://www.reddit.com/r/DnDBehindTheScreen/comments/68pwms/dnd_5e_critical_hit_tables_and_fumble_tables/).


Second important part of this file handles encounter generator.
With provided parameters of party size, party level and encounter difficulty, application will do the following:
1. Calculate XP threshold which will be used to determine the content of the encounter.
2. Calculate monsters Challenge Ratings (CR) available for this encouner.
3. Use [Open5e API for DnD SRD content](https://open5e.com/) to retrieve the monsters based on calculated CR.
4. It will sort the monsters per CR.
5. It will generate encounter by adding one monster at a time until XP threshold is reached.

### Presentation
Presentation part of the application is done by using HTML, CSS, Jinja, and Bootstrap.

Folder 'templates' holds all the html pages included in this project.
Core of this implementation is in the **layout.html** file, which holds the template for all the other pages.

Jinja is used to provide a data communication layer between the Controller part and Presentation part.

Bootstrap is used to make the visual aspect of the application more appealing and standardized.

### Resources and links
**Database data**: [Reddit post by u/freeWeemsy](https://www.reddit.com/r/DnDBehindTheScreen/comments/68pwms/dnd_5e_critical_hit_tables_and_fumble_tables/)

**Monsters data**: [Open5e API for DnD SRD content](https://open5e.com/)

**Images**: Generated by using [Leonardo AI](https://app.leonardo.ai/)
