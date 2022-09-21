# Calories Tracker [![PyPI - Downloads](https://img.shields.io/pypi/dm/caloriestracker?label=Pypi%20downloads)](https://pypi.org/project/caloriestracker/) [![Github - Downloads](https://shields.io/github/downloads/turulomio/caloriestracker/total?label=Github%20downloads )](https://github.com/turulomio/caloriestracker/)

Proyect Archived
================

This project has been archived because I've developed a web app called [django_calories_tracker (backend)](https://turulomio.github.io/django_calories_tracker/) and [calories_tracker (frontend)](https://turulomio.github.io/calories_tracker/) to replace it. These projects improve caloriestracker using vue as a SPA instead of a desktop app with PyQt5. Give it a try ;)

You can still use caloriestracker, it's working fine and it's a good code repository of python with QT.

Links
=====
* [Project web page](https://turulomio.github.io/caloriestracker/)

* [User documentation](https://turulomio.github.io/caloriestracker/doc/CONTENTS.html)

* [API documentation](http://turulomio.users.sourceforge.net/doxygen/caloriestracker/)

* [Pypi web page](https://pypi.org/project/caloriestracker/)

Snapshots
=========
        
<img src="doc/Screenshot_20191029_194701.png" height="200"/> <img src="doc/Screenshot_20191029_194726.png" height="200"/> <img src="doc/Screenshot_20191029_194824.png" height="200"/> <img src="doc/Screenshot_20191029_194920.png" height="200"/> <img src="doc/Screenshot_20191029_195007.png" height="200"/> <img src="doc/Screenshot_20191029_195038.png" height="200"/> 

Install in Linux
================
If you use Gentoo, you can find the ebuild in https://github.com/turulomio/myportage/tree/master/app-office/caloriestracker

If you use another distribution, you nee to install PyQtChart and PyQtWebEngine manually. They aren't in Linux setup.py dependencies due to PyQt5 doesn't use standard setup tools. So for compatibility reasons with distributions like Gentoo, we use this additional step.

`pip install PyQtChart`

`pip install PyQtWebEngine`

`pip install caloriestracker`

Install in Windows
==================

You must download caloriestracker-X.X.X.exe and execute it. They are portable apps so they took a little more time to start, be patient.

Install in Windows with Python
==============================
Install python from https://www.python.org/downloads/ and don't forget to add python to the path during installation.

Open a CMD console

`pip install caloriestracker`

Now you have in the python scripts path `caloriestracker.exe`

If you want to create a Desktop shortcut, for this commands, you can write in console

`caloriestracker_shortcuts`

How to launch Calories Tracker
==============================
Calories Tracker uses PostgreSQL database as its backend. So you need to create a database and load its schema, opening the app with:

`caloriestracker` or pressing it's menu option.

Add your connection settings to a new database and pulse 'New database'

Once database has been created, just log into caloriestracker after typing again:

`caloriestracker` or pressing it's menu option.

Dependencies
============
* https://www.python.org/, as the main programming language.
* https://pypi.org/project/colorama/, to give console colors.
* http://initd.org/psycopg/, to access PostgreSQL database.
* https://pypi.org/project/PyQt5/, as the main library.
* https://pypi.org/project/pytz/, to work with timezones.
* https://pypi.org/project/officegenerator/, to work with LibreOffice and Microsoft Office documents.
* https://pypi.org/project/PyQtChart/, to work with charts.
* https://pypi.org/project/colorama/, to work with colors in console.

How to colaborate with Calories Tracker
=======================================

In Calories tracker you can add your own products and you can share them with us, if you wish with this [PROCEDURE](COLLABORATION.md)

Changelog
=========
0.8.0
  * Removed caloriestracker_init. Now you can create a new database from login.
  * Added sugar to meals tables.
  * Now you can move all data from a personal product to an existing system one.
  * Fixed bugs with empty databases.

0.7.0
  * Food types are now ordered by translated name.
  * Fixed bug deleting a user.
  * Added a combobox to filter products by personal, system and elaborated types.
  * Added meals and foodtype pies.
  * Added curiosities.
  * Added daily meal evolution chart.
  * Calcium component has been added to products.
  * Added copy and paste meals.

0.6.0
  * You can see all products of a company in companies list.
  * You can see a system products without editing.
  * Update a lot files from reusingcode project.
  * Added food types.
  * Added additives.
  * Added russian translations. Thanks DankanTsar.
  * Added product mantainer mode. Only for developers.
  * Added more products.
  * Added glutenfree field.
  * This version hasn't database issue documented [here](https://github.com/turulomio/caloriestracker/blob/master/doc/DATABASE_ISSUES.md)

0.5.0
  * Now you can find translated strings
  * Formats are now translated
  * Improved adding meals and products
  * Elaborated products show information in 100 graims
  * You can delete all meals from a selected day
  * Added meals I eat the most
  * Added more products

0.4.0
  * Calories Traker init executable is working again
  * Replaced QSpinwidgets to a personalized widget
  * Added format multipliers
  * Now you can report an issue from inside Calories Tracker
  * Improved products translations
  * Added more products

0.3.0
  * frmAbout user interface improved
  * Translations of hardcoded strings improved
  * Charts are improved
  * Added more curiosities
  * Added more products, companies and formats

0.2.0
  * Added formats, elaborated products
  * Updated to PyQt5-5.13.1
  * Improved spanish translation
  * Added users management
  * Improved contribution process
  * Added weight and height charts
  * Added more reused code

0.1.0
  * First version
