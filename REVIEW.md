# CODE REVIEW for 🤖RoboTurtle🐢

By Sebastiaan van der Laan as final project as part of WebApps, minor programmeren.


## Room for improvement

Below I have listed the current situation and some possible improvements to code and repository structure.
Numbered, abstract ideas are detailed further with an example directly below them.


|  | Currently | Ideally |
|---|-----------|-------------|
| 1 | A decent repository structure. | A perfectly neat, logical repository structure that seperates all concerns into different files/folders and has only one main app/python file.
| * | Application.py is the main file that handles flask routing, spotify user authorization via API and calls upon certain RoboTurtle functions. roboturtle.py handles all further API requests, the sql database and the sql database. | A main file that delegates different functionalities to seperate files in different folder(s): seperating at least flask routing, both authorization and other spotify API requests, sql database queries.
| 2 | Each file mainly serves a specific purpose, but there is some overlap between functionalities. | The purpose of each file is abundantly clear and the top class/function within serves that exact purpose, in turn served by the functions directly below (or in other, assisting files). |
| * | For instance: application.py depends upon few different RoboTurtle functions instead of depending on a class/subclass/function as a whole. | One main app depends only on a class (or classes) to do their bidding, possibly with different parameters, but does not call upon specific functions of a class. |
| 3 | No seperate security folder/files. | A clear seperation of security matters from the rest of the code. |
| * | oAuth Spotify API authorization is handled by the main application.py | A clear seperation of the (oAuth) authorization from everything else, including other API matters.|
| 4 | Internal and external data handled in broadly the same manner, by the same file. | Delegation and seperation of internal and external data. |
| * | The same roboturtle.py handles Spotify API requests and its own SQL database, without external files for either. | A clear seperation of handling own database and external spotify API matters into different files. |
| 5 | Insufficient abstraction. | Perfectly efficient, abstract top level code, with all impertinent details tucked away in lower files or even the sql database. |
| * | The different metrics a user can choose to change what recommendations to request are hardcoded into a form on templates/turtlemode, and are hardcoded into the POST route to be retrieved from that form upon request. | A sql database table containing all those metrics to be able to generate (part of) that form and for the route to distill any value from that form to pass onto the RoboTurtle and its recommendations function as **kwargs. |
| 6 | Neat comments. | Code so clear that comments are superfluous except to explain particular usage/parameters etc.
