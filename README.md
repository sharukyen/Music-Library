# COMPSCI 235 Starter Repository for Assignment 2
This is a starter repository for the assignment 2 of CompSci 235 in Semester 2, 2022.


## Description

A track browsing web application that uses Python's flask framework. 
The application makes use of libraries such as the Jinja's templating library to build the front end.
Architectural design patterns and principles including building the service layer, Repository  and the application uses Flask Blueprints to segment the components that makes up the application. 
Testing features includes unit and end-to-end testing using the pytest tool.

## Cloning the Repo

On your computer navigate to the directory where you want the app to be located.
eg. In terminal(mac) or Git Bash shell
```shell 
$ cd Documents/Webapps
```
Then clone the GitHub Repo:
eg. In terminal(mac) or Git Bash shell
```shell
$ git init
$ git clone https://github.com/UoA-CS-Sindhwani-CS235-S2-2022/cs235_2022_assignment-nwu939_swu694.git
```

## Installation

**Installation via requirements.txt**
Once in the desired directory run the commands below in terminal(mac) or Command Prompt

```shell
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File'->'Settings' and select your project from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment. 

## Execution

**Running the application**

From the project directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 


## Testing

After you have configured pytest as the testing tool for PyCharm (File - Settings - Tools - Python Integrated Tools - Testing), you can then run tests from within PyCharm by right clicking the tests folder and selecting "Run pytest in tests".

Alternatively, from a terminal in the root folder of the project, you can also call 'python -m pytest tests' to run all the tests. PyCharm also provides a built-in terminal, which uses the configured virtual environment. 

## Configuration
The cs235_2022_assignment-nwu939_swu694/.env file contains variable settings. They are set with appropriate values.

FLASK_APP: Defines Entry point of the application (wsgi.py).
FLASK_ENV: The environment in which to run the application (either development or production).
TESTING: Set to False for running the application. Overridden and set to True automatically when testing the application.
 
## Data sources

The data files are modified excerpts downloaded from:
https://www.loc.gov/item/2018655052  or
https://github.com/mdeff/fma 

We would like to acknowledge the authors of these papers for introducing the Free Music Archive (FMA), an open and easily accessible dataset of music collections: 

Defferrard, M., Benzi, K., Vandergheynst, P., & Bresson, X. (2017). FMA: A Dataset for Music Analysis. In 18th International Society for Music Information Retrieval Conference (ISMIR).

Defferrard, M., Mohanty, S., Carroll, S., & Salathe, M. (2018). Learning to Recognize Musical Genre from Audio. In The 2018 Web Conference Companion. ACM Press.
